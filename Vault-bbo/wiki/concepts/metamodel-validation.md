---
title: "Metamodel Validation"
type: concept
tags: [metamodel-validation, q2-coefficient, cross-validation, surrogate-quality, predictivity]
created: 2026-05-10
updated: 2026-05-10
sources: [Iooss-2010-Q2-Metamodel-Validation.md, Sacks-1989-DACE.md]
---

Metamodel (surrogate) validation assesses how well a surrogate model predicts simulator outputs at unobserved inputs. Before trusting a surrogate to guide optimization, validation confirms the model's predictive accuracy in the relevant input domain.

## The Q2 Predictivity Coefficient

Q2 is the standard scalar metric for surrogate quality, analogous to R² but computed on held-out (not training) data:

```
Q2 = 1 - Σᵢ (y(xᵢ) - Ŷ₋ᵢ(xᵢ))² / Σᵢ (y(xᵢ) - ȳ)²
```

**Leave-one-out (LOO) Q2**: each point is held out and predicted by a model trained on the rest. Computationally efficient for kriging (analytic LOO formula); for XGBoost, use k-fold CV instead.

| Q2 | Interpretation for ISP use |
|----|--------------------------|
| > 0.99 | Safe to trust for optimization |
| 0.95–0.99 | Good; validate top candidates before deployment |
| 0.80–0.95 | Cautious; targeted retraining needed in optimization region |
| < 0.80 | Unreliable; do not guide optimizer with this surrogate |

## Why This Matters for the ISP Workflow

The XGBoost model trained on 300k register configurations has never been formally Q2-validated. It is possible that:
- Q2 is high globally (300k samples is large) but low in the CMA-ES search region
- Q2 differs across IQ metrics (MTF may be harder to predict than false color)

**Recommended action**: compute k-fold Q2 on the existing 300k dataset per metric. If Q2 < 0.95 in the region CMA-ES is exploring, trigger the targeted retraining loop ([[active-learning]]).

## Regional vs. Global Q2

Global Q2 (computed over the full 200D input space) can be high even if local prediction quality near the optimum is poor. For optimization guidance, **regional Q2** — computed on points near the current CMA-ES mean — is more informative.

```python
# Regional Q2: compute only on points within 2σ of CMA-ES current mean
mask = np.all(np.abs(X - cma_mean) < 2 * cma_sigma, axis=1)
q2_regional = cross_val_score(model, X[mask], y[mask], cv=5, scoring='r2').mean()
```

## Validation Design

If validation data must be collected (not just reusing training data), the optimal design places validation points maximally distant from training points ([[iooss-2010-q2-metamodel-validation]]). This identifies worst-case prediction regions with fewer evaluations than random validation sets.

## See also

- [[iooss-2010-q2-metamodel-validation]]
- [[active-learning]]
- [[surrogate-model]]
- [[sacks-1989-dace]]
- [[isp-register-optimization]]
