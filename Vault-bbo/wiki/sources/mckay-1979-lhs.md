---
title: "A Comparison of Three Methods for Selecting Values of Input Variables (McKay, Beckman & Conover, 1979)"
type: source
tags: [latin-hypercube-sampling, experimental-design, space-filling, sampling, computer-experiments]
created: 2026-05-10
updated: 2026-05-10
sources: [McKay-1979-LHS.md]
---

**Authors**: M.D. McKay, R.J. Beckman, W.J. Conover (Los Alamos Scientific Laboratory / Texas Tech)
**Year**: 1979 (reprinted Technometrics 2000, Vol. 42)
**URL**: asc.ohio-state.edu/statistics/comp_exp/jour.club/McKayConoverBeckman.pdf

## Summary

Introduces Latin Hypercube Sampling (LHS) as a space-filling design for computer experiments. Proves that LHS yields lower variance estimators than random (Monte Carlo) sampling for a broad class of estimators, and demonstrates the advantage on a real nuclear safety simulation. LHS is the standard starting design for any surrogate model in high-dimensional spaces.

## Three Sampling Methods Compared

| Method | Description | Variance |
|--------|-------------|---------|
| **Random sampling** | iid draws from F(x) | Baseline |
| **Stratified sampling** | partition into J strata, sample proportionally | ≤ random |
| **Latin Hypercube** | divide each dimension into N equal-probability strata, sample once per stratum, randomly permute across dimensions | ≤ stratified (for monotone functions) |

## Latin Hypercube Construction

For K input variables and N desired samples:
1. Divide the range of each variable X_k into N equiprobable intervals
2. Draw one sample from each interval for each variable: gives N values per dimension
3. Randomly permute (match) the N values across dimensions

Result: every variable has exactly one sample in each stratum (full marginal coverage), and columns are combined randomly to avoid structured patterns.

**Key theorem**: If f(x) is monotone in each argument, `Var(LHS estimator) ≤ Var(random estimator)`. The improvement is substantial when the function's output is driven by only a few of the inputs.

## Why LHS Beats Random Sampling for ISP

With 200 ISP registers, random sampling leaves large empty regions in each dimension's range. LHS guarantees that all portions of every register's range are represented in the training set. With 300k points:

- **Random sampling**: some register ranges may be severely under-sampled; the XGBoost surrogate will extrapolate in these regions
- **LHS**: every register's full range is covered, making the surrogate more reliable for the optimizer

If future data collection is planned, LHS should be used for each sampling round. Existing 300k data was likely random; augmenting with targeted LHS samples in sparse regions would improve surrogate quality.

## See also

- [[latin-hypercube-sampling]]
- [[surrogate-model]]
- [[sacks-1989-dace]]
- [[iooss-2010-q2-metamodel-validation]]
- [[isp-register-optimization]]
