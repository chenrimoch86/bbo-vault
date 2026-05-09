---
title: Mermaid Diagram Demo
type: analysis
tags: [demo, mermaid, visualization, bayesian-optimization, llm-bo-hybrid]
created: 2026-05-08
updated: 2026-05-08
sources: []
---

Demonstration of Mermaid diagram types using real wiki content.
Open this file in Obsidian to see rendered diagrams.

---

## 1. Flowchart — The BO Core Loop

```mermaid
flowchart TD
    A([Start]) --> B["Space-filling design<br/>Latin hypercube / Sobol"]
    B --> C["Fit surrogate<br/>Gaussian Process"]
    C --> D["Maximize acquisition function<br/>EI / UCB / PI"]
    D --> E["Evaluate true function<br/>at selected point"]
    E --> F{"Budget<br/>exhausted?"}
    F -- No --> C
    F -- Yes --> G([Return best observed point])
```

---

## 2. Taxonomy — LLM–BO Integration Patterns

```mermaid
flowchart LR
    ROOT["LLM × Optimization<br/>Hybrids"] --> P1["LLM as Optimizer<br/>OPRO"]
    ROOT --> P2["LLM as Surrogate"]
    ROOT --> P3["Adaptive Switching"]
    ROOT --> P4["LLM Evolves Algorithms<br/>LLaMEA-BO"]
    ROOT --> P5["Expert-Block Small LLMs<br/>TCS / Naphade 2025"]

    P2 --> P2a["Zero-shot warmstart<br/>LLAMBO"]
    P2 --> P2b["Fine-tuned on BO trajectories<br/>GPTOpt / Llama 3.1"]

    P3 --> P3a["Uncertainty-gated switching<br/>BORA"]
    P3 --> P3b["Federated-style weighting<br/>LLINBO"]
```

---

## 3. State Diagram — BORA Adaptive Switching

```mermaid
stateDiagram-v2
    [*] --> LLM_Leads : High GP uncertainty\n(σ_mean > θ_high)
    LLM_Leads --> LLM_Filters : Medium uncertainty\n(θ_low < σ_mean ≤ θ_high)
    LLM_Filters --> Vanilla_BO : Low uncertainty\n(σ_mean ≤ θ_low)
    Vanilla_BO --> LLM_Leads : Plateau detected\nor uncertainty rises
    LLM_Leads --> LLM_Leads : Update trust score\nfrom outcome
    LLM_Filters --> LLM_Filters : BO candidates\nfiltered by LLM
```

---

## 4. Concept Map — Key Relationships

```mermaid
flowchart TD
    BO["[[bayesian-optimization]]\nBayesian Optimization"]
    GP["[[gaussian-process]]\nGaussian Process\nO(n³) surrogate"]
    AF["[[acquisition-function]]\nEI / UCB / PI / REI"]
    TR["[[trust-region-bo]]\nTrust-Region BO\nTuRBO · AdaScale · MG-TuRBO · REI"]
    HD["[[high-dimensional-bo]]\nHigh-Dimensional BO\nD > 20"]
    SM["[[surrogate-model]]\nSurrogate Models\nGP · NN · MARS · RBF"]
    LLM["[[llm-bo-hybrid]]\nLLM–BO Hybrids"]
    CMA["[[cma-es]]\nCMA-ES\nEvolution Strategy"]
    HPO["[[hyperparameter-optimization]]\nHPO"]

    BO -->|uses| GP
    BO -->|guided by| AF
    BO -->|scales via| TR
    BO -->|addresses| HD
    GP -->|is a| SM
    TR -->|solves| HD
    LLM -->|augments| BO
    LLM -->|replaces| GP
    CMA -->|alternative to| BO
    BO -->|applied to| HPO
    LLM -->|applied to| HPO
```

---

## 5. Timeline — Trust-Region BO Evolution

```mermaid
timeline
    title Trust-Region BO Lineage
    2019 : TuRBO (Eriksson) : NeurIPS · multi-armed bandit restarts
    2024 : REI (Namura) : Regional EI · TR optimality guarantee · Fujitsu
    2026 : AdaScale-TuRBO : GP degeneracy diagnosis · scaled lengthscale prior
    2026 : MG-TuRBO : Memory-guided restarts · basin clustering · 84D traffic
```

---

## 6. Quadrant — LLM Surrogate Trade-offs

```mermaid
quadrantChart
    title LLM–BO Hybrids: Cost vs Data Regime
    x-axis Low data --> High data
    y-axis Low cost --> High cost
    quadrant-1 High cost, data-rich
    quadrant-2 High cost, data-scarce
    quadrant-3 Low cost, data-scarce
    quadrant-4 Low cost, data-rich
    LLAMBO: [0.2, 0.75]
    BORA GPT-4o-mini: [0.5, 0.45]
    GPTOpt Llama 3.1: [0.25, 0.3]
    TCS phi4 local: [0.35, 0.15]
    LLaMEA-BO: [0.45, 0.65]
    LLINBO: [0.6, 0.5]
```

---

## See also

- [[bayesian-optimization]]
- [[llm-bo-hybrid]]
- [[trust-region-bo]]
- [[gaussian-process]]
- [[acquisition-function]]
