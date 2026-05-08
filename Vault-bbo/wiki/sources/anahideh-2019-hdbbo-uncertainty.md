---
title: "High-Dimensional BBO under Uncertainty (Anahideh et al., 2019)"
type: source
tags: [high-dimensional, black-box-optimization, uncertainty, mars, variable-selection, noise]
created: 2026-05-08
updated: 2026-05-08
sources: [Anahideh-2019-HDBBO-Uncertainty.md]
---

**Authors**: Anahideh et al.
**Year**: 2019

## Summary

Identifies two practical gaps in high-dimensional BBO: (1) the presence of unimportant (irrelevant) input variables that dilute the search, and (2) uncertainty (noise) in black-box output evaluations. Proposes two complementary methods: **TK-MARS** for variable screening and **Smart-Replication** for noise-robust sampling.

## TK-MARS (Tree-Knot MARS)

[[surrogate-model]] based on MARS (Multivariate Adaptive Regression Splines) with a tree-knot partitioning extension.

**Key properties**:
- **Non-interpolating**: unlike kriging/GP, TK-MARS smooths observations rather than passing through them, making it naturally robust to noise.
- **Variable screening**: the partitioning structure inherently identifies and de-emphasizes unimportant dimensions.
- **Partitioning**: divides the input space into non-overlapping regions and fits local polynomial models.

Addresses gap (1): high-dimensional BBO with many irrelevant variables — where GP's ARD lengthscales can struggle.

## Smart-Replication

An adaptive sampling strategy for noisy BBO.

**Key properties**:
- **Noise-level agnostic**: does not require knowledge of the noise variance σ²; adapts based on observed inconsistency.
- **Adaptive replication**: concentrates replicated evaluations (re-evaluations of the same point) at promising regions, reducing uncertainty where it matters most for acquisition decisions.
- **Promising-point focus**: identifies points with high improvement potential and replicates preferentially there.

Addresses gap (2): uncertain/noisy black-box outputs that confound standard BO's surrogate fitting.

## See also

- [[high-dimensional-bo]]
- [[surrogate-model]]
- [[bayesian-optimization]]
- [[gaussian-process]]
