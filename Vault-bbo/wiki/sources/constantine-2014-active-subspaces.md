---
title: "Active Subspace Methods in Theory and Practice (Constantine, Dow & Wang, 2014)"
type: source
tags: [active-subspaces, dimension-reduction, kriging, uncertainty-quantification, high-dimensional]
created: 2026-05-10
updated: 2026-05-10
sources: [Constantine-2014-Active-Subspaces.md]
---

**Authors**: Paul G. Constantine (Colorado School of Mines), Eric Dow, Qiqi Wang (MIT)
**Year**: 2014
**URL**: arxiv.org/pdf/1304.2070

## Summary

Active subspace methods detect the low-dimensional directions of strongest variability in a high-dimensional function using gradient evaluations. Rather than ranking coordinate axes (as Sobol/Morris do), active subspaces discover *rotated* directions that capture the function's dominant variation. The paper provides theoretical error bounds, links theory to kriging, and demonstrates 100D → low-D reduction for a PDE model.

## Core Method

Given a function f(x) with m inputs, define the m×m matrix:

```
C = E[∇f(x) · ∇f(x)ᵀ]  (uncentered gradient covariance)
```

Eigendecompose C = WΛWᵀ. The eigenvectors W define rotated coordinates:
- **Active variables y = W₁ᵀx** (corresponding to large eigenvalues) — directions where f varies most
- **Inactive variables z = W₂ᵀx** (small eigenvalues) — directions where f is nearly flat

Build a response surface on y only: f(x) ≈ g(W₁ᵀx). If n ≪ m, this is a massive dimensionality reduction.

## Active Subspace vs. Sensitivity Analysis

| Method | Finds | Requires | For ISP |
|--------|-------|----------|---------|
| Sobol/Morris | Important coordinate axes | Many simulator runs | Identifies top registers |
| **Active subspaces** | Important linear combinations of axes | Gradient evaluations | Finds correlated register groups |
| SHAP | Surrogate feature importance | Trained model | Fastest; uses XGBoost |

Active subspaces are most valuable when the important directions are *diagonal* in register space — i.e., when combinations of registers (e.g., all sharpening registers together) matter more than individual ones. This is plausible for ISP blocks.

## Gradient Requirement and ISP Applicability

The method requires gradient evaluations ∇f(x). For the ISP pipeline:
- **Direct gradients are unavailable** (black-box C++ simulator)
- Finite differences approximate gradients but need m+1 = 201 evaluations per gradient sample
- With 300k existing data and the XGBoost surrogate, gradients can be computed analytically via the surrogate (XGBoost doesn't support gradients natively, but SHAP interaction values provide a related decomposition)

**Practical path**: compute active subspace on the XGBoost surrogate using surrogate gradients (finite differences on the surrogate are cheap). This approximates the true active subspace.

## See also

- [[high-dimensional-bo]]
- [[sensitivity-analysis]]
- [[surrogate-model]]
- [[isp-register-optimization]]
