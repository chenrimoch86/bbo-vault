---
title: High-Dimensional Bayesian Optimization
type: concept
tags: [high-dimensional, bayesian-optimization, curse-of-dimensionality, scalability]
created: 2026-05-08
updated: 2026-05-08
sources: [Gonzalez-2024-HDBO-Survey.md, Wang-2018-EBO.md, AdaScale-TuRBO-2026.md, Scalable-NN-BBO-2025.md, Anahideh-2019-HDBBO-Uncertainty.md]
---

High-dimensional Bayesian Optimization (HDBO) addresses the failure modes of standard [[bayesian-optimization]] when the input dimension D exceeds roughly 10–20. The challenges compound: GP degeneracy, acquisition intractability, and exponential search space growth all worsen with D.

## Core Challenges

**GP degeneracy** — In D dimensions, pairwise distances between n random points concentrate around Θ(L√D). With fixed kernel lengthscales, the kernel matrix approaches near-identity, making the GP behave like independent noise ([[adascale-turbo-2026]] quantifies this via Maximum Information Gain).

**Acquisition optimization** — Maximizing EI/UCB over [0,1]^D is an inner non-convex optimization that becomes intractable as D grows.

**Curse of dimensionality** — Exponentially more samples needed to cover the domain; uninformative regions dominate.

**O(n³) GP scaling** — Exacerbated when large n is needed to compensate for high D.

## Strategy Taxonomy (Gonzalez et al., 2024)

[[gonzalez-2024-hdbo-survey]] (NeurIPS 2024 D&B) organizes HDBO methods into 7 families:
1. **Variable selection** — identify and optimize only the active subset of dimensions.
2. **Additive models** — decompose f(x) = Σ f_m(x_{A_m}); optimize per-component ([[wang-2018-ebo]]).
3. **Trust regions** — local GP within an adaptive hyperrectangle ([[trust-region-bo]]).
4. **Linear embeddings** — project to a low-D subspace (REMBO, ALEBO).
5. **Nonlinear embeddings** — VAE or other learned maps to latent space.
6. **Gradient information** — exploit gradient oracles if available.
7. **Structured spaces** — specialized kernels for sequences, graphs (protein engineering, drug design).

## Selected Methods

| Method | Strategy | Dimension Range | Notes |
|--------|----------|-----------------|-------|
| TuRBO | Trust region + multi-armed bandit | 14D–200D | [[trust-region-bo]] |
| AdaScale-TuRBO | Trust region + scaled GP prior | 50D–100D | [[adascale-turbo-2026]] |
| EBO | Additive GP + Mondrian partitions | 10K observations | [[wang-2018-ebo]] |
| SNBO | NN surrogate + adaptive region | 10D–102D | [[koratikere-2025-snbo]] |
| TK-MARS | Partitioning + variable screening | High-D, noisy | [[anahideh-2019-hdbbo-uncertainty]] |
| SAASBO | Sparsity-inducing GP priors | High-D | external reference |

## See also

- [[bayesian-optimization]]
- [[trust-region-bo]]
- [[surrogate-model]]
- [[gaussian-process]]
- [[cma-es]]
