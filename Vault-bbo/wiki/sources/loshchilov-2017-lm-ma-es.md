---
title: "LM-MA-ES: Limited-Memory Matrix Adaptation Evolution Strategy (Loshchilov et al., 2017)"
type: source
tags: [cma-es, evolution-strategy, large-scale, limited-memory, black-box-optimization]
created: 2026-05-08
updated: 2026-05-08
sources: [VenkatRamanan-LM-MA-ES.md]
---

**Authors**: Ilya Loshchilov, Tobias Glasmachers, Hans-Georg Beyer
**Year**: 2017 (GECCO)
**Affiliations**: University of Freiburg, Ruhr-Universität Bochum, Vorarlberg University of Applied Sciences
**URL**: arxiv.org/abs/1705.06693

## Summary

LM-MA-ES (Limited-Memory Matrix Adaptation Evolution Strategy) reduces the time and space complexity of CMA-ES from O(n²) to O(n log n) per sample, enabling large-scale black-box optimization in hundreds to thousands of dimensions. It achieves state-of-the-art performance while being conceptually simpler than CMA-ES.

## CMA-ES → MA-ES → LM-MA-ES Progression

**CMA-ES**: maintains n×n covariance matrix C; O(n²) space, O(n²) amortized time.

**MA-ES**: replaces C with a transformation matrix M (representing √C). Removes covariance matrix eigendecomposition; purely multiplicative updates. Identical performance to CMA-ES. Still O(n²).

**LM-MA-ES**: applies limited-memory reduction to MA-ES, inspired by L-BFGS. Instead of maintaining the full M, stores only the k most recent rank-1 update vectors (evolution path history). Matrix-vector products are reconstructed on-the-fly from these vectors.
- **O(n log n)** time and space per sample (with appropriate k = O(log n)).
- Matches state-of-the-art on large-scale benchmarks.

## Key Theoretical Insight

The multiplicative MA-ES update M ← M · (I + c_1·p_σ·p_σᵀ + ...) can be decomposed into a sequence of rank-1 perturbations. By keeping only the k most recent perturbation vectors and reconstructing M implicitly, the same search distribution quality is maintained at a fraction of the cost.

## Adversarial Input Demonstration

The paper demonstrates LM-MA-ES on **generating adversarial inputs for a random forest classifier** — a black-box, non-smooth, high-dimensional problem. This illustrates the algorithm's value for ML-related BBO tasks beyond the traditional continuous optimization benchmarks.

## See also

- [[cma-es]]
- [[nikolaus-hansen]]
- [[high-dimensional-bo]]
