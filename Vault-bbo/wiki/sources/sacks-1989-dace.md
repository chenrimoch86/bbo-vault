---
title: "Design and Analysis of Computer Experiments (Sacks et al., 1989)"
type: source
tags: [surrogate, gaussian-process, kriging, experimental-design, computer-experiments]
created: 2026-05-10
updated: 2026-05-10
sources: [Sacks-1989-DACE.md]
---

**Authors**: Jerome Sacks, William J. Welch, Toby J. Mitchell, Henry P. Wynn
**Year**: 1989
**Venue**: Statistical Science, Vol. 4, No. 4
**URL**: stat.duke.edu/courses/Spring14/sta961.01/ref/SackWelcMitcWynn1989.pdf

## Summary

The foundational paper for surrogate modeling of expensive deterministic computer simulations. Establishes the **DACE** (Design and Analysis of Computer Experiments) framework: model simulator output as a realization of a Gaussian stochastic process, design experiments (choose inputs) via space-filling criteria, and use the resulting kriging predictor as a cheap substitute. Every subsequent surrogate-based optimization paper — including [[bartz-beielstein-2016-surrogate-bbo]] and the Gaussian Process literature — traces to this work.

## Core Framework

**Problem**: A computer code `y = f(x)` is expensive to run. We want to predict `f` at unobserved inputs from n observations.

**Key insight**: Treat the deterministic output as a realization of a stochastic process:
```
Y(x) = f(x) = μ(x) + Z(x)
```
where `Z(x)` is a zero-mean stationary Gaussian process with covariance `σ² R(xi, xj)`.

**Predictor**: The BLUP (Best Linear Unbiased Predictor) = kriging predictor:
```
Ŷ(x*) = f̂(x*) + r(x*)ᵀ R⁻¹ (y - Fβ̂)
```
This gives both a point prediction and an analytic uncertainty estimate (kriging variance).

## Why Space-Filling Design Matters

Because the simulator is deterministic, classical statistical designs (replication, factorial) are wasteful. Space-filling designs like Latin Hypercube Sampling ([[mckay-1979-lhs]]) spread observations evenly across the input space to minimize worst-case prediction error. The paper demonstrates that space-filling outperforms random sampling for fitting kriging predictors.

## Relevance to ISP Surrogate

The ISP pipeline is exactly the "expensive deterministic computer code" DACE addresses. The 300k (register, IQ) training set is a de facto DACE experiment (though likely not LHS-designed). Key implications:
- If future data collection rounds are planned, LHS over the 200D register space will give better surrogate coverage than random sampling
- XGBoost replaces the kriging predictor in practice, but the design-of-experiments principles remain identical
- The Q2 validation metric ([[iooss-2010-q2-metamodel-validation]]) formalizes DACE's "predictivity" concept

## See also

- [[surrogate-model]]
- [[gaussian-process]]
- [[latin-hypercube-sampling]]
- [[metamodel-validation]]
- [[bartz-beielstein-2016-surrogate-bbo]]
