---
title: "Surrogate-Based Optimization: A Tutorial (Bartz-Beielstein & Zaefferer, 2016)"
type: source
tags: [survey, surrogate-model, design-of-experiments, bayesian-optimization, rbf, kriging]
created: 2026-05-08
updated: 2026-05-08
sources: [Bartz-Beielstein-Surrogate-BBO.md]
---

**Authors**: Thomas Bartz-Beielstein, Martin Zaefferer
**Venue**: International Transactions in Operational Research (ITOR), 2016
**URL**: (survey article)

## Summary

A pedagogical survey of surrogate-based optimization covering the full pipeline from initial sampling through surrogate selection to infill criterion and search region management. Serves as a foundational reference for the practical implementation of [[bayesian-optimization]] and related methods.

## Key Contributions

**Design of Experiments (DOE)**
- Full/fractional factorial designs, Latin hypercube designs (LHD) with maximin distance criterion, Sobol quasi-random sequences.
- LHD with maximin distance is the standard choice for initializing BO; Sobol provides better uniformity for moderate dimensions.

**Surrogate Model Taxonomy**
- Polynomial response surfaces (linear, quadratic): fast, no uncertainty.
- RBF: linear, cubic, thin-plate spline, multiquadric, Gaussian basis functions. Global approximator.
- Kriging / GP: interpolating probabilistic model; foundation of EGO. See [[gaussian-process]].
- SVM regression: useful for limited data.
- Mixed / ensemble surrogates.

**Infill Criteria (Merit Functions)**
- EI (Expected Improvement): E[max(f(x)−f*,0)]; the basis of EGO.
- Probability of Improvement (PI).
- Lower Confidence Bound (LCB).
- Gutmann bumpiness: penalizes points near existing samples; global diversity.
- MRS weighted score: combines surrogate value with model uncertainty.
- See [[acquisition-function]].

**Discrete/Mixed-Integer BBO**
- SO-MI (surrogate optimization with mixed-integer): handles categorical and integer variables.
- SO-I (integer only): extends Kriging to integer domains.

## See also

- [[surrogate-model]]
- [[gaussian-process]]
- [[acquisition-function]]
- [[bayesian-optimization]]
- [[high-dimensional-bo]]
