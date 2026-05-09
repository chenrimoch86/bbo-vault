---
title: "Multi-Objective Optimization"
type: concept
tags: [multi-objective, pareto, nsga-ii, qehvi, trade-off, scalarization]
created: 2026-05-10
updated: 2026-05-10
sources: [Deb-2002-NSGA-II.md, Daulton-2020-qEHVI.md]
---

Multi-objective optimization finds solutions that trade off between multiple competing objectives simultaneously, rather than combining them into a single scalar. The result is a **Pareto front**: a set of solutions where no objective can be improved without worsening another.

## Relevance to ISP Register Optimization

The ISP problem has three objectives: maximize MTF, minimize false color, minimize desaturation. These conflict: sharpening that improves MTF often increases false color. The current approach uses a fixed weighted sum, pre-committing to one trade-off point. True multi-objective optimization returns all Pareto-optimal register configurations.

## Pareto Dominance and Pareto Front

Solution A **dominates** solution B if A is at least as good on all objectives and strictly better on at least one. The **Pareto front** is the set of non-dominated solutions. For ISP, the Pareto front shows: "if you want MTF=X, the best achievable false color and desaturation are Y and Z."

## Methods

### NSGA-II (GA-based)
**Source**: [[deb-2002-nsga-ii]]

Evolutionary approach: runs a population through nondominated sorting + crowding distance selection. Returns an approximate Pareto front after many generations.

- Pros: no surrogate needed; handles any number of evaluations; naturally returns a population of trade-off solutions
- Cons: GA inefficiency on continuous spaces (no covariance learning); needs ~100–1000 generations × population to converge

### qEHVI (Bayesian Optimization-based)
**Source**: [[daulton-2020-qehvi]]

Extends Expected Improvement to multi-objective case via expected hypervolume improvement. Uses GP surrogates per objective.

- Pros: sample-efficient for expensive evaluations; handles batch parallel evaluation
- Cons: requires GP with O(n³) cost; doesn't scale to 300k training points directly

### Weighted Sum (Current Approach)
Collapses objectives into `w₁·MTF - w₂·false_color - w₃·desaturation`. Finds one point on the Pareto front per run. Simple but requires specifying trade-off weights in advance.

## Scalarization vs. True Multi-Objective

| Approach | Weight needed | Solutions returned | ISP use case |
|----------|--------------|-------------------|-------------|
| Weighted sum | Yes | 1 per run | Production (single target per product) |
| NSGA-II | No | Full Pareto front | Exploration, multi-product |
| qEHVI | No | Full Pareto front | Expensive evaluation regime |

For ISP product development, running NSGA-II (with XGBoost as surrogate proxy evaluator) to map the Pareto front once enables informed selection of weight vectors for subsequent CMA-ES runs.

## Hypervolume Indicator

The volume of objective space dominated by the Pareto front (below a reference point). Used as the single scalar measure of Pareto front quality: larger hypervolume = better coverage of the trade-off surface. qEHVI maximizes expected hypervolume improvement per evaluation.

## See also

- [[deb-2002-nsga-ii]]
- [[daulton-2020-qehvi]]
- [[image-quality-metrics]]
- [[cma-es]]
- [[isp-register-optimization]]
