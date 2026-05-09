---
title: "SALib: An Open-Source Python Library for Sensitivity Analysis (Herman & Usher, 2017)"
type: source
tags: [sensitivity-analysis, sobol-indices, morris-screening, salib, python]
created: 2026-05-10
updated: 2026-05-10
sources: [Herman-2017-SALib.md]
---

**Authors**: Jon Herman (UC Davis), Will Usher (University of Oxford)
**Year**: 2017
**Venue**: Journal of Open Source Software, 2(9), 97
**URL**: joss.theoj.org/papers/10.21105/joss.00097.pdf

## Summary

SALib is a Python library implementing global sensitivity analysis (SA) methods for simulation models. It covers Sobol indices, Morris screening, FAST, Delta, DGSM, and Fractional Factorial methods. For ISP register analysis, **Morris screening** and **Sobol indices** are the two methods of direct interest: Morris identifies which of the 200 registers matter with few simulator runs; Sobol quantifies exact variance contribution per register.

## Morris Screening (Elementary Effects)

Morris screening is a cheap one-factor-at-a-time method for ranking inputs:
- Generates a sample of "trajectories" through the input space
- For each trajectory, changes one input at a time and measures the effect
- Reports `μ*` (mean absolute elementary effect) and `σ` (standard deviation) per input

**Cost**: ~(k+1)·r evaluations where k=inputs and r=trajectories (typically r=10–50)
**For 200 registers**: ~2000–10,000 evaluations to screen all registers

Morris identifies the "dead" registers (μ* ≈ 0) vs. "influential" registers — the first-pass filter before more expensive analysis.

## Sobol Indices

Sobol indices decompose total output variance into contributions from each input and their interactions:
- **First-order index Sᵢ**: fraction of variance due to register i alone
- **Total index STᵢ**: fraction of variance due to register i including all interactions

**Cost**: (2k+2)·N evaluations (N=512–2048 typically). For 200 registers: ~200k evaluations.
**Upside**: Sobol gives exact variance partition — if STᵢ < 0.01, register i is truly ignorable.

## SALib vs. SHAP for Register Analysis

| Method | Cost | What it measures | Best for |
|--------|------|-----------------|----------|
| Morris | ~2k evals (cheap) | Ranking/screening | First pass, identify dead registers |
| Sobol | ~400k evals | Exact variance partition | Confirming which registers matter |
| [[lundberg-2018-treeshap|TreeSHAP]] | Free (post-training) | Surrogate feature importance | Register ranking from trained XGBoost |

For this project, TreeSHAP is the lowest-cost option since the XGBoost model is already trained. Sobol on the actual simulator would give ground-truth variance decomposition but requires ~400k additional simulator runs.

## See also

- [[sensitivity-analysis]]
- [[lundberg-2017-shap]]
- [[lundberg-2018-treeshap]]
- [[isp-register-optimization]]
- [[cpp-register-profiling-workflow]]
