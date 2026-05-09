---
title: LLM–BO Integration Patterns
type: analysis
tags: [llm, bayesian-optimization, hybrid, surrogate, acquisition-function]
created: 2026-05-08
updated: 2026-05-08
sources: [Yang-2023-OPRO.md, Liu-2024-LLAMBO.md, Meindl-2025-GPTOpt.md, BORA-2025.md, Chang-2025-LLINBO.md, Li-2025-LLaMEA-BO.md, TCS-2025-Small-LLMs-HPT.md]
---

Synthesis of how LLMs are integrated into [[bayesian-optimization]] loops and what improvements each pattern delivers.

## Pattern 1 — LLM as Optimizer

**Paper:** [[yang-2023-opro]] (Google DeepMind, 2023)

LLM receives a meta-prompt containing prior `(solution, score)` pairs and generates new candidates directly. No [[gaussian-process]] involved. Applied to prompt optimization, linear regression, and TSP.

**Improvement:** +8% on GSM8K, +50% on BBH prompt optimization tasks.

```mermaid
flowchart TD
    A([Start]) --> B["Describe problem<br/>in natural language"]
    B --> C["Build meta-prompt<br/>with prior solution+score pairs"]
    C --> D["LLM generates<br/>new candidates"]
    D --> E["Evaluate candidates<br/>on true objective"]
    E --> F{"Budget<br/>exhausted?"}
    F -- No --> C
    F -- Yes --> G([Return best candidate])
```

---

## Pattern 2 — LLM as Surrogate

**Papers:** [[liu-2024-llambo]] (ICLR 2024), [[meindl-2025-gptopt]]

LLM predicts `f(x)` from few-shot examples in natural language, replacing the GP [[surrogate-model]]. LLAMBO also performs zero-shot warmstarting, eliminating the cold-start problem. GPTOpt fine-tunes Llama 3.1 8B on 2M BO trajectories to produce `mean ± std` estimates and select via EI.

**Improvement:** strongest in the **early/data-scarce regime** where a GP has too few observations to fit reliably.

```mermaid
flowchart TD
    A([Start]) --> B{Warmstart?}
    B -- Yes\nLLAMBO --> C["Zero-shot candidate sampling<br/>from LLM prior"]
    B -- No --> D["Few-shot prompt<br/>with observed x, f-x pairs"]
    C --> D
    D --> E["LLM predicts<br/>mean ± std for candidates"]
    E --> F["Select next point<br/>via EI over LLM output"]
    F --> G[Evaluate true function]
    G --> H{"Budget<br/>exhausted?"}
    H -- No --> D
    H -- Yes --> I([Return best point])
```

---

## Pattern 3 — Adaptive Switching

**Papers:** [[huo-2025-bora]] (IJCAI 2025), [[chang-2025-llinbo]] (U. Michigan)

The system dynamically decides who leads based on GP uncertainty:

- **BORA:** high σ_mean → LLM leads; medium → LLM filters BO candidates; low → vanilla BO. ~$5 total cost (GPT-4o-mini).
- **LLINBO:** gradually reduces LLM weight as GP accumulates data (federated-style weighting). Theoretical guarantees on regret.

**Improvement:** best of both worlds — LLM handles exploration and plateaus, GP handles exploitation as data grows.

```mermaid
flowchart TD
    A[Fit GP on observations] --> B{"Check GP<br/>uncertainty σ_mean"}
    B -- High σ\nLLM leads --> C["LLM proposes<br/>next candidate"]
    B -- Medium σ\nLLM filters --> D["BO proposes candidates<br/>LLM selects best"]
    B -- Low σ\nGP confident --> E["Vanilla BO<br/>maximize acquisition"]
    C --> F[Evaluate true function]
    D --> F
    E --> F
    F --> G[Update GP + trust score]
    G --> H{"Plateau<br/>detected?"}
    H -- Yes --> C
    H -- No --> A
```

---

## Pattern 4 — LLM Evolves the Algorithm

**Paper:** [[li-2025-llamea-bo]]

Population-based (µ+λ ES) where LLM generates complete Python BO algorithm classes. Crossover and mutation via prompting. The LLM is not a component inside BO — it designs the optimizer itself.

**Improvement:** outperforms BO baselines on 19/24 BBOB benchmark functions in 5D; generalizes across dimensions.

```mermaid
flowchart TD
    A([Start]) --> B["LLM generates initial<br/>population of BO algorithm classes"]
    B --> C["Evaluate each algorithm<br/>on benchmark functions"]
    C --> D[Select top µ algorithms]
    D --> E["LLM crossover:<br/>merge two parent algorithms"]
    E --> F["LLM mutation:<br/>modify one algorithm via prompt"]
    F --> G["Add λ offspring<br/>to population"]
    G --> H{"Generations<br/>exhausted?"}
    H -- No --> C
    H -- Yes --> I([Return best BO algorithm class])
```

---

## Pattern 5 — Expert-Block for Small LLMs

**Paper:** [[naphade-2025-tcs-hpt]] (IIT Roorkee)

A Trajectory Context Summarizer (TCS) converts raw training logs into structured state reports, enabling small local models (phi4:14B, qwen2.5:32B) to match GPT-4 within 0.9pp on 6 [[hyperparameter-optimization]] tasks.

**Improvement:** **near-zero marginal cost**, fully private, on-device inference.

```mermaid
flowchart TD
    A["Raw training logs<br/>metrics, loss curves"] --> B["TCS Expert Block<br/>Trajectory Context Summarizer"]
    B --> C["Structured state report<br/>in natural language"]
    C --> D["Small local LLM<br/>phi4 14B / qwen2.5 32B"]
    D --> E["Suggest next<br/>hyperparameter config"]
    E --> F["Train model<br/>with suggested config"]
    F --> G["Append result<br/>to training log"]
    G --> A
```

---

## Cross-Cutting Insights

- **LLM advantage shrinks with data:** LLINBO shows GP surpasses LLM surrogate as observations accumulate. LLMs are most valuable **early** or at **plateaus**.
- **Cost spectrum:** GPT-4o-mini at ~$5 total (BORA) vs. locally-run 14B models (TCS) at near-zero marginal cost.
- **Interpretability:** GPTOpt's GP-mimicking outputs are verifiable; OPRO's prompt trajectory is inspectable.

## See also

- [[llm-bo-hybrid]]
- [[bayesian-optimization]]
- [[gaussian-process]]
- [[acquisition-function]]
- [[surrogate-model]]
- [[hyperparameter-optimization]]
