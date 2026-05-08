---
title: "AdaScale-TuRBO: Diagnosing and Fixing GP Degeneracy in Trust Regions (Tang & Paulson, 2026)"
type: source
tags: [trust-region, bayesian-optimization, gaussian-process, lengthscale, high-dimensional]
created: 2026-05-08
updated: 2026-05-08
sources: [AdaScale-TuRBO-2026.md]
---

**Authors**: Tang & Paulson
**Year**: 2026
**Affiliation**: PaulsonLab
**Code**: github.com/PaulsonLab/AdaScale-TuRBO

## Summary

AdaScale-TuRBO diagnoses the root cause of GP failure inside trust regions and proposes a principled fix. In D-dimensional space with a TR of side length L, pairwise distances between points scale as Θ(L√D). A fixed kernel lengthscale produces near-identity kernel matrices, collapsing the GP into an uninformative model. Scaling the lengthscale prior by L√D resolves this.

## Diagnosis: Maximum Information Gain (MIG)

MIG measures how much the GP prior can explain given n observations. For a degenerate GP (all pairwise correlations near zero), MIG grows linearly with n — each point is treated as fully independent. AdaScale-TuRBO detects this degeneracy through MIG trajectory analysis, providing a quantitative diagnostic for practitioners.

## Fix: Scaled Lengthscale Prior

Replace the fixed lengthscale prior with a **LogNormal prior** with mean:

μ = μ₀ + log(L√D)

where L is the TR side length and D is the dimension. This is refit each time L changes. Prior is estimated via **MAP** (maximum a posteriori) rather than MLE, which better regularizes the lengthscale in small-data regimes.

## Results

Benchmarks (all higher-D than TuRBO's original evaluation):
- Schwefel, Rastrigin, Michalewicz functions in 50D and 100D.
- 60D rover trajectory planning.

AdaScale-TuRBO consistently outperforms: standard TuRBO, D-scaled TuRBO, D-scaled LogEI, and Linear BO.

## Relationship to Other Work

Directly extends [[eriksson-2019-turbo]]. The degeneracy diagnosis generalizes: it applies to any local GP-based method where the region size and dimension interact with the kernel lengthscale. Also relevant to [[high-dimensional-bo]] more broadly.

## See also

- [[trust-region-bo]]
- [[gaussian-process]]
- [[eriksson-2019-turbo]]
- [[high-dimensional-bo]]
