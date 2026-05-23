---
title: CMA-ES and Evolution Strategies
type: concept
tags: [cma-es, evolution-strategy, black-box-optimization, gradient-free]
created: 2026-05-08
updated: 2026-05-23
sources: [CMA-ES-homepage.md, VenkatRamanan-LM-MA-ES.md, Nomura-2024-CMA-ES-Learning-Rate.md, Auger-Hansen-2005-IPOP-CMA-ES.md]
---

The Covariance Matrix Adaptation Evolution Strategy (CMA-ES) is the leading gradient-free, second-order optimization algorithm for continuous black-box problems. It maintains a multivariate Gaussian search distribution N(m, σ²C) and iteratively adapts the mean m, step size σ, and covariance matrix C based on the ranking of sampled candidates.

CMA-ES is the modern descendant of [[evolution-strategies]]: it generalizes ES step-size self-adaptation into adaptation of the *full covariance matrix* (the shape of the search distribution), with CSA automating the step size.

## Key Properties

- **Invariant** to order-preserving (monotonic) transformations of f-values, and to coordinate rotations/translations of the search space.
- **Second-order**: C approximates the inverse Hessian after sufficient adaptation.
- **Quasi-parameter-free**: default hyperparameters (population size λ ≈ 4+3·ln(n), weights, learning rates) work well across problem classes.
- **O(n²) time and space** per generation due to the n×n covariance matrix.

## Standard Update Mechanisms

- **Rank-μ update**: weighted maximum likelihood estimate of the covariance over the top-μ candidates.
- **Rank-1 update (evolution path)**: cumulates the sequence of successful steps to improve conditioning.
- **Cumulative step-size adaptation (CSA)**: adapts σ based on the length of the evolution path p_σ.
- **Negative weights** (CMA with negative update): improves conditioning further.

## Key Variants

**MA-ES** — replaces the covariance matrix C with a transformation matrix M, removing potentially unstable eigendecomposition. Identical performance to CMA-ES; O(n²) but conceptually simpler.

**LM-MA-ES** (Loshchilov et al., 2017) — [[loshchilov-2017-lm-ma-es]]. Applies limited-memory reduction (inspired by L-BFGS) to MA-ES, reducing complexity from O(n²) to **O(n log n)** time and space. State-of-the-art on large-scale benchmarks; demonstrated on adversarial inputs for random forests.

**LRA-CMA-ES** (Nomura et al., 2024) — [[nomura-2024-lra-cma-es]]. Online learning rate η adaptation. Key insight: optimal η ∝ signal-to-noise ratio (SNR). ODE analysis shows small η is needed for multimodal/noisy problems. LRA maintains constant SNR automatically. Does not replace restart strategies for weakly structured landscapes.

**IPOP-CMA-ES** (Auger & Hansen, 2005) — [[auger-hansen-2005-ipop-cma-es]]. Restart CMA-ES, **doubling the population size λ on each restart**, to escape premature convergence on [[multimodal-optimization|multimodal]] landscapes; the population sweep shifts search from local to global. A standard production default (later: BIPOP-CMA-ES).

**Diagonal CMA-ES** — restricts C to diagonal; O(n) but loses rotation invariance.

**MO-CMA-ES** — multi-objective variant.

## CMA-ES vs. Bayesian Optimization

On low-D problems (d < ~15), BO is typically more sample-efficient. Above ~20D, CMA-ES often competes or wins because GP degrades while CMA-ES's covariance adaptation remains effective. TuRBO ([[trust-region-bo]]) was designed specifically to make BO competitive with CMA-ES at high dimensions.

## See also

- [[evolution-strategies]]
- [[differential-evolution]]
- [[bayesian-optimization]]
- [[high-dimensional-bo]]
- [[surrogate-model]]
