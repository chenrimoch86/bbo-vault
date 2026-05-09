---
title: "Latin Hypercube Sampling"
type: concept
tags: [latin-hypercube-sampling, experimental-design, space-filling, sampling, doe]
created: 2026-05-10
updated: 2026-05-10
sources: [McKay-1979-LHS.md, Iooss-2010-Q2-Metamodel-Validation.md]
---

Latin Hypercube Sampling (LHS) is a space-filling experimental design that guarantees coverage of every input variable's range. For k variables and N samples: divide each variable's range into N equal-probability intervals, draw one sample per interval for each variable, then randomly permute to combine across variables.

## Why LHS Beats Random Sampling

With k=200 registers and N=300,000 samples, random sampling in 200D leaves significant gaps in each register's marginal distribution — some value ranges will be under-sampled by chance. LHS ensures:
- **Each register's full range is covered**: every 1/N slice of each dimension has exactly one sample
- **Lower variance**: for monotone functions, LHS variance is strictly less than random sampling
- **Better surrogate fit**: the XGBoost model interpolates less and extrapolates less

The McKay 1979 theorem: if the objective is monotone in each register independently, `Var(LHS) ≤ Var(random)`. For more complex functions, Sobol and scrambled LHS variants are even better.

## LHS in Practice

A basic LHS for N samples, k variables:
```python
from scipy.stats import qmc
sampler = qmc.LatinHypercube(d=200)  # 200 registers
sample = sampler.random(n=300_000)   # N×k matrix, values in [0,1]
# Scale to register bounds
X = qmc.scale(sample, l_bounds, u_bounds)
```

For highest-quality surrogate fitting, use **optimized LHS** (maximin or wrap-around discrepancy criterion) as recommended by [[iooss-2010-q2-metamodel-validation]].

## Relevance to ISP Data Collection

The current 300k training set was likely collected via random sampling (exhaustive or structured experiments). If new data collection rounds are planned:

1. **Use LHS** instead of random for equal cost and better coverage
2. **Adaptive LHS**: identify sparse regions from current data → concentrate new samples there
3. **Augmenting existing data**: use the SHAP-based register ranking ([[sensitivity-analysis]]) to identify which register dimensions most need better coverage, then collect targeted LHS samples

## Optimal LHS Variants

| Criterion | What it optimizes | Best for |
|-----------|------------------|---------|
| Maximin distance | Maximizes minimum distance between points | General surrogate fitting |
| Centered discrepancy | Minimizes centered L² discrepancy | Numerical integration |
| **Wrap-around discrepancy** | Suppresses boundary effects | **GP/kriging metamodels** (recommended by Iooss et al.) |

## See also

- [[mckay-1979-lhs]]
- [[iooss-2010-q2-metamodel-validation]]
- [[sacks-1989-dace]]
- [[surrogate-model]]
- [[isp-register-optimization]]
