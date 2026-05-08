---
title: "Scalable Global Optimization via Local Bayesian Optimization (TuRBO)"
type: source
tags: [trust-region, bayesian-optimization, high-dimensional, multi-armed-bandit, thompson-sampling]
created: 2026-05-08
updated: 2026-05-08
sources: [Eriksson-2019-TuRBO.md]
---

**Authors**: David Eriksson, Michael Pearce, Jacob Gardner, Ryan D. Turner, Matthias Poloczek
**Venue**: NeurIPS 2019
**Affiliation**: Cornell University, Uber AI Labs
**URL**: arxiv.org/abs/1910.01739

## Summary

TuRBO (Trust Region Bayesian Optimization) enables practical [[bayesian-optimization]] for high-dimensional problems by restricting each GP to a local hyperrectangular trust region (TR) around the current best solution. Multiple TRs run in parallel; a Thompson-sampling multi-armed bandit allocates the evaluation budget across them. Author: [[david-eriksson]].

## Methodology

**Trust Region Mechanics**
- Each TR is a hyperrectangle of side length L centered on the incumbent.
- **Expand**: L ← 2L after τ_succ = 3 consecutive successes.
- **Shrink**: L ← L/2 after τ_fail = ⌈d/q⌉ consecutive failures (d = dimension, q = batch size).
- **Restart**: when L < L_min = 2⁻⁷, initialize a new TR from scratch.
- Domain normalized to [0,1]^d; L_init = 0.8, L_max = 1.6.

**Multi-TR Allocation via Thompson Sampling**
- Maintain multiple independent TRs (each with its own incumbent and GP).
- At each step, Thompson-sample from each TR's GP; select the TR whose sample has the highest predicted value.
- Naturally diverse: different TRs explore different basins.

**Results**
- Outperforms CMA-ES, EBO ([[wang-2018-ebo]]), BOCK, BOHAMIANN on all tested benchmarks.
- Benchmarks: robot pushing (14D), rover trajectory (60D), cosmological parameter estimation (12D), lunar landing (12D), Ackley-200D.
- Runtime: < 1 minute per iteration, vs. hours for global BO methods.

## Impact

TuRBO established trust-region local BO as the dominant approach for 20D–200D problems and became the standard baseline for subsequent HDBO work including [[adascale-turbo-2026]], [[mg-turbo-2026]], [[namura-2024-rei]], and [[koratikere-2025-snbo]].

## See also

- [[trust-region-bo]]
- [[bayesian-optimization]]
- [[high-dimensional-bo]]
- [[acquisition-function]]
- [[david-eriksson]]
