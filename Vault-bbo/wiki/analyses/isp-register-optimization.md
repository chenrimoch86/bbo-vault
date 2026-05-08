---
title: ISP Register Optimization — Method Recommendation
type: analysis
tags: [isp, black-box-optimization, high-dimensional, surrogate, cma-es, xgboost, active-subspace]
created: 2026-05-08
updated: 2026-05-08
sources: [Eriksson-2019-TuRBO.md, Koratikere-2025-SNBO.md, Hansen-CMA-ES-Reference.md, Loshchilov-2017-LM-MA-ES.md, Gonzalez-2024-HDBO-Survey.md, Bartz-Beielstein-Surrogate-BBO.md]
---

Recommendation for optimizing ~200 ISP registers across multiple ISP blocks to maximize image quality metrics. Everything runs on the simulator — no real hardware involved.

## Problem Structure

- **Search space:** ~200 continuous registers across multiple ISP blocks
- **Objective:** maximize weighted combination of image quality metrics
- **Pipeline:** Registers → C++ ISP simulator → RGB image → IQ metrics
- **Simulator throughput:** 300 runs/minute via parallel CPUs — the ground truth oracle
- **Training data:** 300,000 simulator runs (registers + IQ metrics), collected in ~16h
- **Current surrogate:** XGBoost trained once on 300k examples, frozen
- **Current optimizer:** genetic algorithm with random starting points over frozen XGBoost

## Current Approach

```mermaid
flowchart LR
    A[300k simulator runs] --> B[Train XGBoost\nsurrogate once]
    B --> C[Freeze XGBoost]
    C --> D[GA with random\nstarting points]
    D --> E[Best predicted config]
```

## Weak Points

1. **GA in continuous 200D** — GA is designed for discrete/combinatorial problems. In continuous high-D space it converges poorly and gets stuck in local optima.
2. **Random starting points** — spread poorly in 200D; many starts explore redundant regions.
3. **Frozen surrogate, no validation loop** — XGBoost is never checked against the simulator after training. GA may find a region where XGBoost is wrong, and the final config is never validated.
4. **Full 200D search** — most registers have minimal effect on most metrics. Searching all 200 simultaneously dilutes optimization budget.

## Sensitivity Analysis: XGBoost Feature Importance

No additional simulator runs needed. XGBoost computes per-register importance natively from the existing trained model.

```mermaid
flowchart LR
    A[Trained XGBoost\n300k examples] --> B[Feature importance\ngain per register per metric]
    B --> C[Rank registers\nby importance]
    C --> D[Keep top registers\n~20-40 of 200]
    D --> E[Active subspace\nfor optimization]
```

Use **gain** importance (contribution to metric improvement at each split) rather than frequency. Run separately per metric to understand which registers drive which IQ dimensions.

Cross-reference with C++ static analysis: registers read by ISP blocks with no path to target metrics can be eliminated before even running XGBoost importance.

## Recommended Approach: Multi-Start CMA-ES + Iterative Refinement

Replace GA with **[[cma-es]]** (CMA-ES). CMA-ES is specifically designed for continuous high-D optimization — it adapts its search covariance matrix to the landscape geometry as it explores.

```mermaid
flowchart TD
    A[XGBoost feature importance\n+ C++ static analysis] --> B[Active subspace\n~20-40 registers]
    B --> C[Multi-start CMA-ES\nN random starting points\nover frozen XGBoost]
    C --> D[XGBoost inference\nmicroseconds per query\nmillions of queries free]
    D --> E[Top-K candidate configs\nacross all CMA-ES starts]
    E --> F[Validate top-K\non simulator\n300/min = minutes]
    F --> G{XGBoost matches\nsimulator?}
    G -- Yes --> H([Best validated config])
    G -- No\ndisagreement region --> I[Sample 5000 configs\naround disagreement\n~17 minutes]
    I --> J[Retrain XGBoost\non 300k + new targeted points]
    J --> C
```

## CMA-ES vs GA

```mermaid
flowchart LR
    subgraph GA ["Genetic Algorithm"]
        G1[Random population] --> G2[Crossover + mutation\nblind to landscape]
        G2 --> G3[Selection]
        G3 --> G2
    end
    subgraph CMA ["CMA-ES"]
        C1[Random start] --> C2[Sample from\nN·m·C·]
        C2 --> C3[Evaluate + rank]
        C3 --> C4[Update mean + covariance\nadapts to landscape shape]
        C4 --> C2
    end
```

| | GA | CMA-ES |
|---|---|---|
| Designed for | Discrete / combinatorial | Continuous high-D |
| Adapts to landscape | No | Yes — covariance matrix |
| Starting points | Random, unstructured | Structured multi-start |
| XGBoost queries | Limited by population size | Millions, free |
| Local optima | Gets stuck | Multi-start escapes |

For large-scale continuous problems, use **[[loshchilov-2017-lm-ma-es]]** (LM-MA-ES) which runs in O(n log n) — better suited if operating on the full 200D space.

## Iterative Refinement Loop

The simulator at 300/min makes the validation loop nearly free:

```mermaid
flowchart TD
    A[CMA-ES finds\noptimum region] --> B[Validate top-100\nconfigs on simulator\n~20 seconds]
    B --> C{Agreement\n> threshold?}
    C -- Yes --> D[Best config confirmed]
    C -- No --> E[Identify disagreement\nregion in register space]
    E --> F[Sample 5000 configs\nin that region\n~17 minutes]
    F --> G[Retrain XGBoost]
    G --> A
```

Each iteration costs minutes. Run until XGBoost reliably matches the simulator in the high-performance region.

## MG-TuRBO Internal Flow (Reference)

Included for reference — MG-TuRBO is not the recommended method here (wrong regime for 300/min throughput), but documents the trust-region approach considered earlier.

```mermaid
flowchart TD
    A[Initialize trust region TR\naround best known point] --> B[Fit GP surrogate\non all observations]
    B --> C[Maximize acquisition function\nwithin TR bounds]
    C --> D[Evaluate true IQ\nat selected config]
    D --> E[Add observation\nto history]
    E --> F{Did TR\nimprove?}
    F -- Yes --> G[Expand TR\nL = L × 2]
    F -- No --> H[Shrink TR\nL = L ÷ 2]
    G --> I{L > L_max?}
    H --> J{L < L_min?}
    I -- No --> B
    I -- Yes --> B
    J -- No --> B
    J -- Yes --> K[TR collapsed\ntrigger restart]
    K --> L[Cluster all history\ninto basins via k-means]
    L --> M[Score each basin:\nquality × 1-visitation]
    M --> N[Select restart center\nfrom best underexplored basin]
    N --> A
```

## Summary of Changes from Current Approach

| Aspect | Current | Recommended |
|---|---|---|
| Sensitivity analysis | None | XGBoost feature importance (free) |
| Search space | 200D | 20-40D active registers |
| Optimizer | GA, random starts | Multi-start CMA-ES |
| Surrogate updates | Never | Iterative on simulator disagreement |
| Simulator use | Training data only | Fast validation + targeted retraining |
| Final output | XGBoost-predicted best | Simulator-validated best |

## Why LLM-BO Hybrids Are Not the Right Fit

LLM-BO hybrids are designed for expensive evaluation regimes with very limited data. With 300/min simulator throughput and 300k training examples, this problem is in a different regime entirely — a trained XGBoost surrogate handles the register → metric mapping far better than an LLM.

## See also

- [[Problem_Definition]]
- [[cma-es]]
- [[loshchilov-2017-lm-ma-es]]
- [[high-dimensional-bo]]
- [[surrogate-model]]
- [[koratikere-2025-snbo]]
- [[bayesian-optimization]]
- [[gonzalez-2024-hdbo-survey]]
