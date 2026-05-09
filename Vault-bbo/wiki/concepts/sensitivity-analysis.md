---
title: "Sensitivity Analysis"
type: concept
tags: [sensitivity-analysis, sobol, morris, shap, feature-importance, register-ranking]
created: 2026-05-10
updated: 2026-05-10
sources: [Herman-2017-SALib.md, Lundberg-2017-SHAP.md, Lundberg-2018-TreeSHAP.md]
---

Sensitivity analysis quantifies how much each input variable contributes to variation in the output. For ISP register optimization: identifies which of the ~200 registers strongly influence each IQ metric, enabling targeted optimization and dimension reduction.

## Why Sensitivity Analysis Matters for ISP

With 200 registers and 3 IQ metrics, the optimizer has a 200D search space. Most registers likely have near-zero effect on IQ scores (dead registers: already at optimal values, or truly irrelevant to the active IQ chain). Sensitivity analysis:
1. Identifies dead registers → fix them, reduce search space
2. Ranks active registers → focus CMA-ES on the top ~20–50
3. Reveals register → metric structure → informs per-metric optimization strategy

## Three Methods Available

### Morris Screening (Cheapest)
**Source**: [[herman-2017-salib]]
**Cost**: ~2000–10,000 simulator evaluations
**Output**: μ* (mean effect), σ (variability) per register

First-pass screening: identifies registers with μ* ≈ 0 as dead. Does not quantify exact contributions. Run first.

### Sobol Indices (Ground Truth)
**Source**: [[herman-2017-salib]]
**Cost**: ~400,000 simulator evaluations (for 200 registers)
**Output**: First-order index Sᵢ (individual contribution), Total index STᵢ (including interactions)

Gold standard for variance decomposition. Expensive but gives exact STᵢ < 0.01 → register truly ignorable.

### TreeSHAP (Cheapest, Surrogate-Based)
**Source**: [[lundberg-2018-treeshap]], [[lundberg-2017-shap]]
**Cost**: Seconds (post-training on existing XGBoost model)
**Output**: Per-register, per-sample SHAP values → mean |SHAP| as global importance

**Best starting point** for this project: no additional simulator runs required, uses the already-trained XGBoost on 300k data, gives consistent (not heuristic) importance scores.

## Comparison

| Method | Cost | Consistency | Handles correlated registers? | Ground truth? |
|--------|------|-------------|------------------------------|---------------|
| XGBoost gain | Free | No (inconsistent) | No | No |
| Morris | ~5k evals | Yes | Partial | No |
| Sobol | ~400k evals | Yes | Yes | Yes |
| **TreeSHAP** | Free | **Yes** | **Yes** | Surrogate |

## Recommended Workflow

1. Compute TreeSHAP on XGBoost for each IQ metric → initial register ranking
2. Discard registers with mean |SHAP| < threshold (e.g., bottom 50%)
3. Run Morris screening on simulator to verify dead register identification
4. (Optional) Run Sobol on the top-50 candidates for ground-truth variance decomposition

## See also

- [[herman-2017-salib]]
- [[lundberg-2017-shap]]
- [[lundberg-2018-treeshap]]
- [[constantine-2014-active-subspaces]]
- [[isp-register-optimization]]
- [[cpp-register-profiling-workflow]]
