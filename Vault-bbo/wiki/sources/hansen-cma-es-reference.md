---
title: "CMA-ES Reference Implementation and Tutorial (Hansen)"
type: source
tags: [cma-es, evolution-strategy, reference, tutorial, black-box-optimization]
created: 2026-05-08
updated: 2026-05-08
sources: [CMA-ES-homepage.md]
---

**Author**: Nikolaus Hansen ([[nikolaus-hansen]])
**Resource type**: Reference website + tutorial (cma-es.github.io)
**Python package**: `pycma`

## Summary

The canonical reference for [[cma-es]] maintained by its creator. Covers the algorithm's design rationale, invariance properties, default parameter settings, and practical usage guidance. The `pycma` Python package is the reference implementation used across academic and industrial applications.

## Key Technical Content

**Algorithm Design**
- CMA-ES samples λ ≈ 4 + 3·ln(n) candidates per generation (n = problem dimension).
- Adaptation of mean m (recombination), step size σ (CSA), and covariance matrix C (rank-μ + rank-1 updates).
- Negative covariance update improves convergence on ill-conditioned problems.

**Invariance Properties**
- **Monotonic f-transforms**: performance is identical for any strictly monotonic transformation of f-values (ranks are preserved).
- **Coordinate rotations and translations**: the learned covariance adapts to rotate the search distribution, achieving rotation invariance after sufficient adaptation.
- **Scale transformations**: step-size adaptation maintains scale invariance.

**Parameter Defaults**
- Default hyperparameters (λ, learning rates c_1, c_μ, c_σ, damping d_σ) are derived theoretically and work robustly across problem classes without tuning.
- Population size λ can be increased (restarting with increasing λ, i.e., IPOP-CMA-ES or BIPOP) for multimodal problems.

**Variants Listed**
- CMA-ES with rank-μ only, with negative weights, diagonal CMA-ES.
- MO-CMA-ES (multi-objective).
- xNES (natural evolution strategy) connection.
- LM-CMA-ES (limited memory, O(n log n)); related to [[loshchilov-2017-lm-ma-es]].

## See also

- [[cma-es]]
- [[nikolaus-hansen]]
- [[loshchilov-2017-lm-ma-es]]
- [[high-dimensional-bo]]
