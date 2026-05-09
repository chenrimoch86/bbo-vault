---
title: "Consistent Individualized Feature Attribution for Tree Ensembles — TreeSHAP (Lundberg et al., 2018)"
type: source
tags: [shap, treeshap, xgboost, feature-importance, sensitivity-analysis, explainability]
created: 2026-05-10
updated: 2026-05-10
sources: [Lundberg-2018-TreeSHAP.md]
---

**Authors**: Scott M. Lundberg, Gabriel G. Erion, Su-In Lee (University of Washington)
**Year**: 2018
**URL**: arxiv.org/pdf/1802.03888

## Summary

Derives exact, polynomial-time SHAP values for tree ensemble models (XGBoost, LightGBM, Random Forests). Reduces complexity from exponential `O(TL·2^M)` to `O(TLD²)` where T=trees, L=max leaves, D=max depth, M=features. The algorithm is merged into XGBoost and LightGBM. Also introduces SHAP interaction values and SHAP summary/dependence plots. The practical tool for per-register sensitivity analysis on the ISP XGBoost surrogate.

## Why Gain and Split Count Are Unreliable

The paper formally demonstrates that three popular tree importance methods are **inconsistent**:

- **Gain**: when Model B relies more on a feature than Model A, gain can assign *lower* importance — produces incorrect rankings for correlated features
- **Split count**: number of splits is biased toward features with many near-equal split thresholds
- **Saabas (individualized)**: assigns arbitrary values when features interact

Only SHAP values (and permutation-based methods) are guaranteed consistent. The inconsistency is not rare — it occurs systematically when register features are correlated (which they are in ISP, since multiple registers in the same block jointly affect outputs).

## Tree SHAP Algorithm

For a single tree with depth D and L leaves, Tree SHAP computes exact SHAP values in O(TLD²) vs. naïve O(TL·2^M). Key insight: tree structure allows efficient computation of `E[f(x) | x_S]` for all subsets S by recursively tracking how samples split at each node.

SHAP values are also decomposed into:
- **Main effects**: φᵢ — individual feature contribution
- **SHAP interaction values**: φᵢⱼ — pairwise feature interaction effects

## Practical Use for ISP Register Ranking

```python
import shap
import xgboost as xgb

# train model on 300k (register_config, iq_score) pairs
model = xgb.XGBRegressor().fit(X_train, y_train)

# compute exact SHAP values
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_test)  # shape: (n_samples, n_registers)

# global importance (mean absolute SHAP)
mean_shap = np.abs(shap_values).mean(axis=0)  # one importance per register

# per-metric: run separately for MTF, false_color, desaturation models
```

This gives consistent, interaction-aware importance scores for all 200 registers, enabling reliable ranking and dimension reduction before CMA-ES optimization.

## See also

- [[sensitivity-analysis]]
- [[lundberg-2017-shap]]
- [[chen-2016-xgboost]]
- [[isp-register-optimization]]
- [[cpp-register-profiling-workflow]]
