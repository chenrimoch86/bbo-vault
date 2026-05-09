---
title: "Numerical Studies of the Metamodel Fitting and Validation Processes (Iooss et al., 2010)"
type: source
tags: [metamodel-validation, q2-coefficient, surrogate, kriging, cross-validation, latin-hypercube]
created: 2026-05-10
updated: 2026-05-10
sources: [Iooss-2010-Q2-Metamodel-Validation.md]
---

**Authors**: Bertrand Iooss (EDF R&D), Loïc Boussouf, Vincent Feuillard, Amandine Marrel
**Year**: 2010
**URL**: arxiv.org/pdf/1001.1049

## Summary

Studies two practical challenges in surrogate model construction: (1) which space-filling design leads to the best-fitting Gaussian process metamodel, and (2) how to efficiently estimate metamodel predictivity with a minimum number of validation points. Introduces the **Q2 predictivity coefficient** as the standard metric for surrogate quality, and proposes a sequential validation design for efficient Q2 estimation.

## The Q2 Predictivity Coefficient

Q2 is a leave-one-out cross-validation (LOO-CV) analog of R²:

```
Q2 = 1 - Σᵢ (y(xᵢ) - Ŷ₋ᵢ(xᵢ))² / Σᵢ (y(xᵢ) - ȳ)²
```

where `Ŷ₋ᵢ(xᵢ)` is the surrogate prediction at `xᵢ` trained without that point.

| Q2 range | Interpretation |
|----------|---------------|
| > 0.99 | Excellent; safe to trust surrogate for optimization |
| 0.95–0.99 | Good; minor corrections may be needed |
| 0.80–0.95 | Acceptable; validate top candidates before deploying |
| < 0.80 | Poor; surrogate may mislead the optimizer |

Q2 can be computed efficiently for kriging models analytically. For XGBoost, standard k-fold CV achieves the same purpose.

## Space-Filling Design Recommendation

The paper compares LHS variants optimized by different discrepancy criteria:
- **Maximin distance LHS**: maximizes minimum distance between points
- **Centered discrepancy LHS**: minimizes centered L² discrepancy
- **Wrap-around discrepancy LHS**: suppresses boundary effects

Finding: **wrap-around discrepancy LHS** consistently gives the best metamodel predictivity. Simulated annealing is the recommended optimization algorithm for constructing these designs.

## Sequential Validation Design

Rather than using a fixed held-out test set, the paper proposes an adaptive algorithm that places validation points to maximize information about prediction error — specifically maximizing the distance between validation and learning points. This uses ~30% fewer validation runs than random test sets to achieve the same Q2 estimate accuracy.

## Relevance to ISP Surrogate

The XGBoost model trained on 300k (register, IQ) pairs has never been formally validated with Q2. This is a gap: before trusting XGBoost to guide CMA-ES, a proper LOO-CV or k-fold Q2 should be computed per IQ metric. The paper's threshold (Q2 > 0.95 for safe use in optimization) is the acceptance criterion.

Additionally, if future training rounds are planned, wrap-around discrepancy LHS is the recommended design.

## See also

- [[metamodel-validation]]
- [[latin-hypercube-sampling]]
- [[surrogate-model]]
- [[sacks-1989-dace]]
- [[chen-2016-xgboost]]
- [[isp-register-optimization]]
