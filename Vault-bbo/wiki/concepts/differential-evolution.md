---
title: Differential Evolution (DE)
type: concept
tags: [differential-evolution, evolutionary-algorithm, global-optimization, continuous-optimization]
created: 2026-05-23
updated: 2026-05-23
sources: [Storn-Price-1997-Differential-Evolution.md, Hrstka-2009-EA-Competitive-Comparison.md]
---

Differential Evolution (DE) is a population-based, real-valued global optimizer introduced by Storn & Price ([[storn-price-1997-differential-evolution]]). Often grouped with the [[genetic-algorithm]], it is in practice a sibling of [[evolution-strategies]] for continuous spaces, and one of the standard non-Bayesian baselines to benchmark against [[cma-es]].

## The differential mutation

DE's signature operator perturbs a vector with the *scaled difference of two other population members*:

```
v = x_r1 + F · (x_r2 − x_r3)        (DE/rand/1)
u = binomial-crossover(v, x_target; CR)
x_target ← u  iff  cost(u) < cost(x_target)   (greedy selection)
```

Because the difference vector automatically shrinks as the population converges and grows on flat regions, DE **self-scales** its steps — its analogue to ES step-size self-adaptation, but derived from the population's own geometry rather than an explicit strategy parameter.

## Control parameters

Only three, which is DE's main practical appeal:
- **NP** — population size (≈ 5·D–10·D).
- **F** — differential weight (≈ 0.5; range ~0.4–1).
- **CR** — crossover rate (0.1 robust; 0.9–1.0 faster on separable problems).

Variants follow the `DE/base/n-diffs/crossover` naming, e.g. `DE/rand/1/bin` (baseline), `DE/best/2/bin`.

## Strengths and limits

- **Strengths:** few parameters, robust, easily parallelized, strong on nonlinear / non-differentiable / multimodal continuous functions; beat simulated-annealing and GA/ES contenders in the original 1997 study.
- **Limit:** the classic form scales poorly. The independent benchmark [[hrstka-2009-ea-comparison]] found DE robust at moderate dimension but **failing past ~30–50D**, and attributed its relative weakness to the *absence of a dedicated mutation operator* — hybrids that add one (e.g. SADE) scale better.

## See also

- [[genetic-algorithm]]
- [[evolution-strategies]]
- [[cma-es]]
- [[rainer-storn]], [[kenneth-price]]
