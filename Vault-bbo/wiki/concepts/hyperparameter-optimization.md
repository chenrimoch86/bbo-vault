---
title: Hyperparameter Optimization
type: concept
tags: [hyperparameter-optimization, automl, bayesian-optimization, llm]
created: 2026-05-08
updated: 2026-05-08
sources: [Liu-2024-LLAMBO.md, TCS-2025-Small-LLMs-HPT.md, BORA-2025.md, Li-2025-LLaMEA-BO.md, Wang-2025-LLM-Agent-HPO.md, Meindl-2025-GPTOpt.md]
---

Hyperparameter Optimization (HPO, also HPT for tuning) finds the configuration of ML training settings — learning rate, batch size, network architecture, regularization strengths — that maximizes model performance on a validation set. Each trial requires training a full model: the function is expensive, black-box, and noisy.

## Formulation as BBO

HPO is a canonical [[bayesian-optimization]] application. Each hyperparameter configuration h ∈ H is evaluated by training the model and measuring validation accuracy. The optimization budget (number of trials) is typically 10–100.

## Standard Approaches

**Grid and random search** — exhaustive or random sampling of the configuration space. Simple; does not exploit prior evaluations.

**Bayesian Optimization** — [[gaussian-process]] surrogate + EI/UCB acquisition. Strong sample efficiency; standard choice in Optuna, HyperOpt, SMAC. Variant: TPE (Tree-structured Parzen Estimator) replaces GP with density estimation over "good" vs. "bad" observations.

**AutoML pipelines** — automate the full ML pipeline (preprocessing, feature engineering, model selection, HPO). Examples: Auto-sklearn, TPOT, NAS frameworks.

## LLM-Based Approaches

LLMs bring prior knowledge about common hyperparameter settings and optimization strategies, valuable when trials are extremely expensive.

| Method | Model | Mechanism | Key Result |
|--------|-------|-----------|------------|
| LLAMBO ([[liu-2024-llambo]]) | GPT-3.5/4 | LLM as surrogate + warmstarting | Best in sparse-data regime |
| BORA ([[huo-2025-bora]]) | GPT-4o-mini | Adaptive LLM/BO switching | ~$5 total; 7 real tasks |
| TCS ([[naphade-2025-tcs-hpt]]) | phi4:14B, qwen2.5:32B | TCS expert block | Within 0.9pp of GPT-4; local |
| GPTOpt ([[meindl-2025-gptopt]]) | Llama 3.1 8B (fine-tuned) | GP-mimicking LLM surrogate | d≤10, N≤50 regime |
| LLaMEA-BO ([[li-2025-llamea-bo]]) | GPT-4 | LLM evolves BO algorithm classes | 19/24 BBOB functions |

## Key Trade-offs

- **Large proprietary LLMs** (GPT-4): high capability, high cost, privacy concerns.
- **Small local LLMs** with expert blocks (TCS): near-GPT-4 quality at near-zero marginal cost; requires deterministic context preprocessing.
- **Fine-tuned LLMs** (GPTOpt): best in-domain performance but requires training data (2M trajectories).

## See also

- [[bayesian-optimization]]
- [[llm-bo-hybrid]]
- [[gaussian-process]]
- [[surrogate-model]]
