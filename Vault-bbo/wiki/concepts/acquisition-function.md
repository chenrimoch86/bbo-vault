---
title: Acquisition Function
type: concept
tags: [acquisition-function, bayesian-optimization, exploration-exploitation]
created: 2026-05-08
updated: 2026-05-08
sources: [Bartz-Beielstein-Surrogate-BBO.md, Eriksson-2019-TuRBO.md, Namura-2024-REI.md, Wang-2018-EBO.md]
---

An acquisition function (also: merit function, infill criterion) guides the sequential sampling strategy in [[bayesian-optimization]]. It uses the [[gaussian-process]] posterior — mean μ(x) and variance σ²(x) — to score candidate points, trading off exploration (high uncertainty) against exploitation (high predicted value).

## Standard Acquisition Functions

**Expected Improvement (EI)** — E[max(f(x) − f*, 0)] where f* is the current best. Analytic for GP posteriors; the basis of the EGO algorithm (Efficient Global Optimization). The most widely used criterion in practice.

**Probability of Improvement (PI)** — P(f(x) > f*). Simpler than EI; tends toward exploitation.

**Lower/Upper Confidence Bound (LCB/UCB)** — μ(x) ± β·σ(x). β controls exploration-exploitation trade-off; used in bandit-theory BO analyses (GP-UCB with cumulative regret bounds).

**Thompson Sampling** — draw a sample path from the GP posterior and select its maximum. Used in TuRBO ([[eriksson-2019-turbo]]) for multi-trust-region bandit allocation; naturally diverse across parallel TR evaluations.

**Gutmann Bumpiness / MRS** — penalize proximity to existing samples; favors global diversity. Covered in the [[bartz-beielstein-2016-surrogate-bbo]] survey.

## Regional Expected Improvement (REI)

Proposed by [[namura-2024-rei]] (Fujitsu, AAAI 2025): identifies **regions** (not points) with high probability of containing the global optimum. Theoretically proven to select the optimal trust region. Addresses stagnation in local optima without assuming problem structure. Integrates with TuRBO.

## Acquisition in High Dimensions

Maximizing the acquisition function over [0,1]^D is itself a non-convex optimization problem. Strategies:
- **Local optimization** within a trust region (TuRBO, AdaScale-TuRBO).
- **Thompson sampling** — bypasses explicit maximization.
- **Ensemble / partition-based** — EBO uses per-additive-component maximization.

## See also

- [[bayesian-optimization]]
- [[gaussian-process]]
- [[trust-region-bo]]
- [[high-dimensional-bo]]
