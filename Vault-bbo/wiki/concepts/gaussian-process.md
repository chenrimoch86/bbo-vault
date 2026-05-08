---
title: Gaussian Process
type: concept
tags: [gaussian-process, surrogate, probabilistic-model, kernel]
created: 2026-05-08
updated: 2026-05-08
sources: [Bartz-Beielstein-Surrogate-BBO.md, Eriksson-2019-TuRBO.md, Wang-2018-EBO.md, AdaScale-TuRBO-2026.md]
---

A Gaussian Process (GP) is a probabilistic, non-parametric surrogate model used extensively in [[bayesian-optimization]]. It defines a distribution over functions such that any finite collection of function values has a joint Gaussian distribution.

## Definition

A GP is fully specified by a mean function μ(x) and a covariance (kernel) function κ(x, x'). Given observations D_n = {(x_t, y_t)}, the GP posterior provides:
- **Posterior mean** μ_n(x): the best point estimate of f(x).
- **Posterior variance** σ²_n(x): the model's uncertainty at x.

These two quantities directly power [[acquisition-function]] computation (EI, UCB, etc.).

## Common Kernels

- **Matérn-5/2**: widely used in BO; less smooth than RBF, more realistic for physical functions. With ARD (automatic relevance determination), learns per-dimension lengthscales.
- **RBF/Squared Exponential**: infinitely smooth; over-smooth for many engineering problems.
- **Matérn-3/2, 1/2**: rougher functions; used when observations are noisy.

## Computational Complexity

Training a GP requires inverting the n×n kernel matrix: **O(n³) time, O(n²) space**. This becomes a bottleneck beyond ~1,000–10,000 observations. Sparse GPs (inducing points) and random feature approximations partially address this.

## High-Dimensional Degeneracy

In D dimensions, pairwise distances between n random points concentrate around Θ(L√D), where L is the trust region side length. If the kernel lengthscale is fixed, the kernel matrix approaches near-independence (all off-diagonal entries near zero), causing the GP to behave like an independent noise model. [[adascale-turbo-2026]] diagnoses this and proposes scaling the lengthscale prior by L√D.

## GP as Surrogate vs. Alternatives

- **RBF / Polynomial**: faster but no uncertainty estimate; see [[surrogate-model]].
- **Neural networks**: scale better to high-D and large-N; no native uncertainty without BNNs; see [[koratikere-2025-snbo]] and [[meindl-2025-gptopt]].
- **MARS/TK-MARS**: partitioning-based, variable screening capability; see [[anahideh-2019-hdbbo-uncertainty]].

## See also

- [[bayesian-optimization]]
- [[acquisition-function]]
- [[surrogate-model]]
- [[high-dimensional-bo]]
- [[adascale-turbo-2026]]
