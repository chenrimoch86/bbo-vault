---
title: "BORA: Language-Based Bayesian Optimization Research Assistant (IJCAI 2025)"
type: source
tags: [llm, bayesian-optimization, adaptive, trust-mechanism, real-world]
created: 2026-05-08
updated: 2026-05-08
sources: [BORA-2025.md]
---

**Authors**: Huo et al.
**Venue**: IJCAI 2025
**Year**: 2025

## Summary

BORA (Bayesian Optimization Research Assistant) is a hybrid [[llm-bo-hybrid]] framework with an adaptive policy that switches between LLM-led and standard BO modes based on the current state of the [[gaussian-process]] surrogate. A trust mechanism updates the LLM's influence score from outcomes; a plateau detector triggers LLM intervention when BO stagnates.

## Adaptive Heuristic Policy

Policy is conditioned on **σ_mean** — the average GP posterior standard deviation (mean uncertainty) across the domain:

| σ_mean level | Action |
|---|---|
| High (high overall uncertainty) | **a2**: LLM leads; generates new candidate points using domain knowledge |
| Medium (moderate uncertainty) | **a3**: LLM filters BO candidates; selects best subset from GP-proposed points |
| Low (GP confident) | **a1**: vanilla BO; standard acquisition function maximization |

The rationale: when the GP is highly uncertain (few observations, early phase), LLM prior knowledge is most valuable. When the GP is confident, it should dominate.

## Trust Mechanism

- LLM starts with a neutral trust score.
- After each LLM intervention, the outcome (whether the LLM's suggestion led to an improvement) updates the score.
- Low trust score → less LLM involvement; high trust score → more.
- Prevents over-reliance on a miscalibrated LLM.

## Self-Consistency

- 3 LLM outputs generated per intervention; majority vote or best-of-3 selection.
- Reduces variance in LLM suggestions.

## Cost

- Uses GPT-4o-mini; total cost ~$5 for a full optimization run.
- Versus $41 for LAEA (a more expensive LLM-based alternative).

## Benchmarks

Branin (2D), Levy-10D, Ackley-15D, and four real-world problems: Solar panel placement (4D), Pétanque (7D), Sugar Beet optimization (8D), Hydrogen Production (10D).

## See also

- [[llm-bo-hybrid]]
- [[bayesian-optimization]]
- [[acquisition-function]]
- [[gaussian-process]]
- [[hyperparameter-optimization]]
