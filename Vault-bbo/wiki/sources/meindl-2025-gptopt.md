---
title: "GPTOpt: Fine-Tuned LLM as BO Surrogate (Meindl et al., 2025)"
type: source
tags: [llm, bayesian-optimization, fine-tuning, surrogate, expected-improvement]
created: 2026-05-08
updated: 2026-05-08
sources: [Meindl-2025-GPTOpt.md]
---

**Authors**: Meindl et al.
**Year**: 2025

## Summary

GPTOpt fine-tunes Llama 3.1 8B on 2,000,000 [[bayesian-optimization]] trajectories that include [[gaussian-process]] surrogate outputs. The result is an LLM that produces GP-like mean±std estimates for candidate points and selects the next query via Expected Improvement (EI). Operates in a conversational format: the LLM iteratively proposes candidates with uncertainty estimates and selects the best.

## Methodology

**Training Data**
- 2M BO trajectories generated with GP surrogate feedback.
- Each trajectory step: (optimization history, candidate) → (GP posterior mean, GP posterior std).
- Fine-tuning teaches the LLM to mimic GP posterior inference from context.

**Inference Loop**
- LLM receives: task description + history of (x, f(x)) pairs in natural language.
- LLM produces: mean±std estimates for candidate points.
- Acquisition: standard EI computed from LLM-produced mean±std; selects next evaluation point.

**Regime**: d ≤ 10 dimensions, N ≤ 50 observations. Designed for the small-data, low-dimensional HPO setting typical of ML hyperparameter search.

## Key Properties

**Interpretability**: the surrogate outputs (mean and std) are explicit and verifiable, unlike opaque LLM-generated rankings or direct suggestions. Users can inspect what the LLM "believes" about each candidate.

**No GP Required**: the entire BO loop runs through the LLM; no external GP library needed.

**Conversational format**: naturally iterative; fits agentic LLM deployment patterns.

## Results

Outperforms traditional BO optimizers and LLM-BO baselines (including LLAMBO [[liu-2024-llambo]]) in the d≤10, N≤50 regime.

## Limitations

- Regime is restricted to low-D, small-N; scales poorly with dimension.
- Fine-tuning on 2M trajectories requires significant compute upfront.

## See also

- [[llm-bo-hybrid]]
- [[bayesian-optimization]]
- [[gaussian-process]]
- [[hyperparameter-optimization]]
- [[liu-2024-llambo]]
