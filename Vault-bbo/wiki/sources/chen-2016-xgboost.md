---
title: "XGBoost: A Scalable Tree Boosting System (Chen & Guestrin, 2016)"
type: source
tags: [xgboost, gradient-boosting, surrogate, machine-learning, feature-importance]
created: 2026-05-10
updated: 2026-05-10
sources: [Chen-2016-XGBoost.md]
---

**Authors**: Tianqi Chen, Carlos Guestrin (University of Washington)
**Year**: 2016
**Venue**: KDD 2016
**URL**: arxiv.org/pdf/1603.02754

## Summary

XGBoost is a scalable, regularized gradient boosted tree system. It introduces a sparsity-aware split algorithm, weighted quantile sketch for approximate tree learning, and careful cache/compression/sharding optimizations to scale to billions of examples. XGBoost is the surrogate model used in this project: trained on 300k (register config, IQ scores) pairs to approximate the expensive ISP pipeline.

## Gradient Boosting Basics

XGBoost fits an additive ensemble of regression trees. At each step t, a new tree is added to minimize:

```
L(t) = Σ l(yi, ŷi(t-1) + ft(xi)) + Ω(ft)
```

where `Ω(ft) = γT + ½λ‖w‖²` regularizes tree complexity (T = leaf count, w = leaf weights). The second-order Taylor expansion of the loss is used to derive optimal leaf weights and split gains analytically.

## Three Feature Importance Types

XGBoost provides three built-in importance metrics:

| Metric | Definition | Notes |
|--------|-----------|-------|
| **Gain** | Total reduction in loss attributed to all splits on this feature | Best for register ranking — measures actual contribution |
| **Cover** | Total number of training samples affected by splits on this feature | Measures breadth of influence |
| **Frequency** | Number of times a feature is used as a split node | Biased toward high-cardinality features |

**Gain is the right metric for register sensitivity ranking.** Frequency is misleading because registers with many near-equal split points get inflated counts. Cover mixes impact with data density.

## Key Technical Innovations Relevant to This Use Case

- **Sparsity-aware algorithm**: handles missing/zero register values without imputation
- **Regularization (λ, α)**: controls overfitting on the 300k training set; important when register → IQ mapping is noisy
- **Feature subsampling**: column subsampling per tree reduces correlation between trees and improves generalization
- **Approximate tree learning**: weighted quantile sketch allows distributed/large-scale fitting

## ISP Surrogate Notes

XGBoost's tree structure makes it naturally interpretable for register analysis. The gain importance rankings identify which ISP registers most strongly influence each IQ metric (MTF, false color, desaturation). However, gain importance is unreliable when registers are correlated — use [[lundberg-2018-treeshap]] SHAP values instead for correlated-feature analysis.

## See also

- [[surrogate-model]]
- [[sensitivity-analysis]]
- [[lundberg-2018-treeshap]]
- [[lundberg-2017-shap]]
- [[iooss-2010-q2-metamodel-validation]]
- [[isp-register-optimization]]
