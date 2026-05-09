---
title: "A Unified Approach to Interpreting Model Predictions — SHAP (Lundberg & Lee, 2017)"
type: source
tags: [shap, feature-importance, explainability, sensitivity-analysis, machine-learning]
created: 2026-05-10
updated: 2026-05-10
sources: [Lundberg-2017-SHAP.md]
---

**Authors**: Scott M. Lundberg, Su-In Lee (University of Washington)
**Year**: 2017
**Venue**: NeurIPS 2017
**URL**: arxiv.org/pdf/1705.07874

## Summary

Introduces SHAP (SHapley Additive exPlanations): a unified framework for model-agnostic feature importance grounded in cooperative game theory. SHAP values are the unique attribution method satisfying local accuracy, missingness, and consistency simultaneously. Unifies six previously independent explanation methods (LIME, DeepLIFT, LRP, Shapley regression, Shapley sampling, QII) under a single theoretical framework.

## Core Concept

SHAP treats each feature as a "player" in a cooperative game where the "payout" is the model prediction. The SHAP value φᵢ for feature i is the average marginal contribution of feature i across all possible subsets of features:

```
φᵢ = Σ_{S⊆F\{i}} |S|!(|F|-|S|-1)!/|F|! · [f(S∪{i}) - f(S)]
```

This Shapley value from game theory is the **only** attribution satisfying:
- **Local accuracy**: Σφᵢ = f(x) - E[f(x)] (attributions sum to prediction)
- **Missingness**: absent features get φ = 0
- **Consistency**: if a model change makes feature i more impactful, φᵢ never decreases

## Why SHAP Beats XGBoost Gain for Register Analysis

Standard XGBoost gain importance is **inconsistent** — a feature can become more important in the model while its gain attribution decreases. This happens with correlated features (correlated ISP registers, e.g., demosaic registers that jointly affect color).

SHAP values correctly account for feature interactions by averaging over all orderings. For the ISP case:
- Gain may over-attribute importance to one register in a correlated group (whichever gets the first split)
- SHAP distributes importance fairly across all correlated registers
- SHAP per-sample values enable detecting which registers matter for specific IQ score regimes

## Model-Agnostic vs. TreeSHAP

The 2017 paper introduces model-agnostic Kernel SHAP (Monte Carlo approximation via sampling). This is slow for large models. [[lundberg-2018-treeshap]] derives exact, O(TLD²) SHAP values for tree ensembles including XGBoost — that is the practical implementation to use.

## See also

- [[sensitivity-analysis]]
- [[lundberg-2018-treeshap]]
- [[chen-2016-xgboost]]
- [[isp-register-optimization]]
