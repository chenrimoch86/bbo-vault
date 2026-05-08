---
title: "Batched Large-scale Bayesian Optimization in High-dimensional Spaces (EBO)"
type: source
tags: [bayesian-optimization, high-dimensional, additive-gp, batch, scalable, ensemble]
created: 2026-05-08
updated: 2026-05-08
sources: [Wang-2018-EBO.md]
---

**Authors**: Zi Wang, Clement Gehring, Pushmeet Kohli, Stefanie Jegelka
**Venue**: AISTATS 2018
**Affiliations**: MIT CSAIL, DeepMind ([[google]])
**URL**: arxiv.org/abs/1706.01445

## Summary

Ensemble Bayesian Optimization (EBO) simultaneously addresses three challenges in BO: large-scale observations (10,000+), high-dimensional inputs, and diverse batch query selection. It is the first method to tackle all three jointly. Key approach: an ensemble of additive [[gaussian-process]] models, each with a randomized partition strategy (Mondrian forest features), producing 2–3 orders of magnitude speedup in posterior inference.

## Key Contributions

**Hierarchical Additive GP with Mondrian Forests**
- Assumes f(x) = Σ f_m(x_{A_m}) over random disjoint partitions of input dimensions.
- Uses Mondrian forest features (tile coding) to approximate the kernel; avoids O(n³) full GP inversion.
- Gibbs sampling over both additive structure and kernel parameters jointly.

**Ensemble + Randomized Inference**
- Maintains a posterior distribution over the ensemble; draws one member per iteration.
- Randomized block approximation of the Gram matrix via Mondrian process; enables parallelization.

**Batch Query Generation**
- Parallelization across blocks automatically generates diverse batch candidates without a separate batch strategy.
- Avoids the quality-diversity tension of explicit batch BO methods.

**Results**
- 400× speedup over state-of-the-art in one experiment.
- Scales to tens of thousands of observations within minutes.
- Applied to real-world problems previously infeasible for BO.

## Limitations

- Additive structure assumption may not hold for all functions.
- Gibbs sampling convergence can be slow for complex posteriors.

## See also

- [[bayesian-optimization]]
- [[gaussian-process]]
- [[high-dimensional-bo]]
- [[surrogate-model]]
