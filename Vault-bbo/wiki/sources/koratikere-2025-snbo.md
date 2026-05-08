---
title: "Scalable Neural Network-Based Blackbox Optimization (SNBO)"
type: source
tags: [neural-network, surrogate-model, high-dimensional, black-box-optimization, scalable]
created: 2026-05-08
updated: 2026-05-08
sources: [Scalable-NN-BBO-2025.md]
---

**Authors**: Pavankumar Koratikere, Leifur Leifsson
**Venue**: Structural and Multidisciplinary Optimization (2025); preprint at arxiv.org/abs/2508.03827
**Affiliation**: Purdue University, School of Aeronautics and Astronautics
**Code**: github.com/ComputationalDesignLab/snbo

## Summary

SNBO proposes a neural network-based [[surrogate-model]] for [[high-dimensional-bo]] that avoids uncertainty estimation entirely, instead using a three-stage infill strategy to balance exploration and exploitation. Evaluated on 10D–102D problems; achieves 40–60% fewer function evaluations and order-of-magnitude runtime reduction compared to GP-based BO baselines.

## Methodology

**Three-Stage Infill Strategy**

1. **Candidate generation (exploration setup)**: create a large candidate set by perturbing the current best point using zero-mean uniform noise whose spread adapts based on optimization progress (analogous to the TR side-length adaptation in TuRBO, [[eriksson-2019-turbo]]).

2. **Exploration set construction**: sequentially select points from the candidate set using a distance-based criterion (from FSSF — Fully Sequential Space-Filling sampling), ensuring diversity in the candidate set.

3. **Exploitation (NN selection)**: apply the trained NN to score all exploration-set candidates; select the q most promising points.

**Adaptive Search Region**
- The perturbation range (r) adapts: expand after successes (up to r_max = 1.6), shrink after failures (down to r_min = 0.025). Maximum success threshold = 3 (mirrors TuRBO's τ_succ).

**No Uncertainty Estimation**
- Unlike Bayesian neural networks (BNN) or NTK-based confidence intervals, SNBO uses the NN purely as a point predictor. Exploration is handled structurally by the distance-based stage, not probabilistically.

## Results

Outperforms four state-of-the-art baselines (including TuRBO) on the majority of test problems across 10D–102D. Benefits particularly evident at large N (many evaluations) where GP's O(n³) scaling becomes prohibitive.

## Relationship to TuRBO

Conceptually inspired by [[eriksson-2019-turbo]] and DYCORS; shares the adaptive region and success/failure counter mechanism but replaces the GP with a NN and replaces Thompson sampling with the explicit 3-stage infill.

## See also

- [[high-dimensional-bo]]
- [[surrogate-model]]
- [[bayesian-optimization]]
- [[gaussian-process]]
- [[trust-region-bo]]
