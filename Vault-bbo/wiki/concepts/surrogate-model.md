---
title: Surrogate Model
type: concept
tags: [surrogate-model, black-box-optimization, approximation, kriging]
created: 2026-05-08
updated: 2026-05-08
sources: [Bartz-Beielstein-Surrogate-BBO.md, Scalable-NN-BBO-2025.md, Meindl-2025-GPTOpt.md, Anahideh-2019-HDBBO-Uncertainty.md]
---

A surrogate model (also: response surface, metamodel, emulator) is a cheap-to-evaluate approximation of an expensive black-box function, built from a set of observed (x, f(x)) pairs. It is the core component of surrogate-based optimization (SBO) and [[bayesian-optimization]].

## Model Families

**Polynomial response surfaces** — low-order polynomials (linear, quadratic). Fast; interpretable; inaccurate for complex multi-modal functions; no uncertainty estimate.

**Radial Basis Functions (RBF)** — weighted combination of radially-symmetric basis functions (linear, cubic, thin-plate spline, multiquadric, Gaussian). Global approximator; no native uncertainty; DYCORS uses RBF for high-D BBO.

**Kriging / Gaussian Process** — interpolating probabilistic model; provides uncertainty estimates essential for [[acquisition-function]] computation. Standard in [[bayesian-optimization]]; O(n³) scaling; see [[gaussian-process]].

**MARS / TK-MARS** — Multivariate Adaptive Regression Splines. Partitioning-based; non-interpolating; performs implicit variable selection. TK-MARS (Tree-Knot MARS, [[anahideh-2019-hdbbo-uncertainty]]) extends this for high-D noisy BBO.

**Support Vector Regression** — SVM applied to regression; useful when training data is limited.

**Neural Networks (NN)** — scale well to large datasets and high dimensions; no native uncertainty. SNBO ([[koratikere-2025-snbo]]) uses NN without uncertainty estimation, relying instead on explicit exploration/exploitation stages. GPTOpt ([[meindl-2025-gptopt]]) fine-tunes an LLM to produce GP-like mean±std estimates.

**Ensemble / mixed surrogates** — combine multiple model types; hedge against mis-specification.

## Choosing a Surrogate

| Criterion | GP | RBF | NN | MARS |
|-----------|----|----|-----|------|
| Uncertainty estimates | Yes | No | No (without BNN) | No |
| High-D scalability | Poor | Moderate | Good | Moderate |
| Large-N scalability | Poor O(n³) | Moderate | Good | Moderate |
| Variable selection | No (ARD lengthscales) | No | Implicit | Yes |

## Role in Design of Experiments

Surrogate quality depends on the initial sample plan: Latin hypercube design (LHD) with maximin distance or Sobol sequences are standard choices, as covered in [[bartz-beielstein-2016-surrogate-bbo]].

## See also

- [[gaussian-process]]
- [[bayesian-optimization]]
- [[high-dimensional-bo]]
- [[acquisition-function]]
