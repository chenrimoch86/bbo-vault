---
title: "Hrstka et al. 2009 — A Competitive Comparison of Different Types of Evolutionary Algorithms"
type: source
tags: [evolutionary-algorithm, differential-evolution, simulated-annealing, benchmark, engineering-optimization]
created: 2026-05-23
updated: 2026-05-23
sources: [Hrstka-2009-EA-Competitive-Comparison.md]
---

O. Hrstka, A. Kučerová, M. Lepš, J. Zeman (Czech Technical University), *"A Competitive Comparison of Different Types of Evolutionary Algorithms"*, arXiv:0902.1647, 2009. A head-to-head benchmark of four stochastic optimizers on artificial and civil-engineering design problems, with a deliberately rigorous methodology (100 runs per case; report success rate *and* mean function evaluations).

## Methods compared

- **DE** — [[differential-evolution]] in the original Storn–Price form ([[storn-price-1997-differential-evolution]]).
- **SADE** — Simplified Atavistic Differential Evolution: a DE/GA hybrid that re-adds mutation and local mutation operators on top of a simplified differential operator.
- **RASA** — Real-coded Augmented Simulated Annealing (real-coded GA operators + Metropolis acceptance + reannealing).
- **IASA** — Integer Augmented Simulated Annealing (integer coding; suited to discrete/combinatorial problems).

## Test problems

Chebyshev polynomial fitting (dim 9), a "type-0" single-narrow-peak function scaled from **dim 1 to 200**, reinforced-concrete beam layout (18 discrete vars), and a periodic-unit-cell composite problem (dim 20).

## Key findings

- **DE is efficient and robust at moderate dimension but degrades sharply with scale.** On the type-0 function it returned N/A (failed) at dims 50, 100, 140, 200, while SADE and RASA solved all dimensions.
- **The mutation operator matters.** SADE markedly outperformed plain DE; the authors attribute this to DE's *lack of a mutation-type operator*, and note that the two strongest methods (SADE, RASA) both use a "local mutation."
- **Restarts/reannealing help.** RASA's edge is credited partly to its reannealing/restart phase — a cheap, effective tool against local minima (echoing the restart logic of [[auger-hansen-2005-ipop-cma-es]]).
- **Real coding beats discrete coding on continuous problems**; IASA was fastest on low-dimensional problems but suffered premature convergence and limited precision at high D.
- All methods share some form of **differential operator**, which the authors call remarkably effective across both real-valued and discrete problems.

**Overall ranking:** SADE most robust for general practical use (best success/parameter trade-off), RASA comparable, DE slightly worse, IASA best only at small scale.

## See also

- [[differential-evolution]]
- [[storn-price-1997-differential-evolution]]
- [[genetic-algorithm]]
- [[evolution-strategies]]
