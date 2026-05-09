---
title: "Differentiable Expected Hypervolume Improvement for Parallel Multi-Objective Bayesian Optimization — qEHVI (Daulton et al., 2020)"
type: source
tags: [multi-objective, qehvi, bayesian-optimization, pareto, botorch, hypervolume]
created: 2026-05-10
updated: 2026-05-10
sources: [Daulton-2020-qEHVI.md]
---

**Authors**: Samuel Daulton, Maximilian Balandat, Eytan Bakshy (Facebook Research)
**Year**: 2020
**Venue**: NeurIPS 2020
**URL**: arxiv.org/pdf (NeurIPS 2020)

## Summary

qEHVI (q-Expected Hypervolume Improvement) is the state-of-the-art multi-objective Bayesian optimization acquisition function. It extends Expected Improvement to multiple objectives by maximizing expected hypervolume improvement — the volume of the dominated hyperspace gained by adding new observations. qEHVI supports parallel (batch) evaluation, is differentiable, and scales to M objectives. Implemented in BoTorch.

## Hypervolume as the Multi-Objective Criterion

The hypervolume indicator measures the volume of the objective space dominated by the current Pareto front (bounded below by a reference point). Maximizing expected hypervolume improvement ensures:
- Each new batch of evaluations maximally expands the Pareto front
- All objectives are treated simultaneously, without scalarization
- Exploration/exploitation balance is handled analytically via the GP posterior

For ISP: the reference point would be (MTF=min_acceptable, false_color=max_acceptable, desaturation=max_acceptable).

## qEHVI vs. Weighted Scalarization vs. NSGA-II

| Method | Requires weight vector? | Efficient at n<500? | Parallel batch? |
|--------|------------------------|-------------------|----------------|
| Weighted sum | Yes | Yes | No |
| NSGA-II | No | No (GA) | Population |
| **qEHVI** | No | **Yes** | Yes (q>1) |

qEHVI is most valuable when evaluations are expensive and you want true Pareto-optimal solutions without committing to a weight vector. For ISP with 300 evals/min, qEHVI's per-sample efficiency advantage over NSGA-II is significant.

## Implementation (BoTorch)

```python
from botorch.acquisition.multi_objective import qExpectedHypervolumeImprovement
from botorch.models import ModelListGP

# Train GP on each objective separately
model = ModelListGP(train_X, train_Y)  # train_Y: (n, 3) for MTF, false_color, desaturation

# Define reference point (worst acceptable values)
ref_point = torch.tensor([mtf_min, fc_max_neg, desat_max_neg])

# Compute qEHVI and optimize
acqf = qExpectedHypervolumeImprovement(model, ref_point=ref_point, partitioning=...)
candidates, _ = optimize_acqf(acqf, bounds=bounds, q=10, ...)
```

## Limitations for ISP Use Case

- Uses GP surrogate internally: O(n³) cost limits applicability beyond ~1000 observations
- For 300k existing data points, GP is infeasible; would need to use the pre-trained XGBoost as surrogate instead, losing the analytic uncertainty estimate that qEHVI requires
- Alternative: use NSGA-II with the XGBoost surrogate as a cheap proxy evaluator

## See also

- [[multi-objective-optimization]]
- [[deb-2002-nsga-ii]]
- [[bayesian-optimization]]
- [[gaussian-process]]
- [[isp-register-optimization]]
