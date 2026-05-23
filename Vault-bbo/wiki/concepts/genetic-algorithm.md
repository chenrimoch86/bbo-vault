---
title: Genetic Algorithm (GA)
type: concept
tags: [genetic-algorithm, schema-theorem, crossover, selection, evolutionary-algorithm]
created: 2026-05-23
updated: 2026-05-23
sources: [Whitley-1994-GA-Tutorial.md, Casas-2015-GA-Multimodal-Review.md]
---

The Genetic Algorithm (GA) is the branch of evolutionary computation that evolves a population of encoded candidate solutions (chromosomes) through **selection, crossover (recombination), and mutation**. Originating with Holland (1975) and popularized as a practical tool by Goldberg and others, its canonical tutorial is [[whitley-1994-ga-tutorial]].

## Canonical loop

1. **Encoding** — represent solutions as fixed-length strings (classically binary; also real-coded, permutation, etc.). Genotype (string) vs. phenotype (decoded solution).
2. **Selection** — bias reproduction toward fitter individuals: fitness-proportionate ("roulette"), or the more robust **rank** and **tournament** selection. (Parent selection *is* fitness-biased here — the key contrast with [[evolution-strategies]].)
3. **Crossover** — recombine parents: one-point, two-point, uniform.
4. **Mutation** — small random changes maintain diversity.
5. Repeat generationally, or one-at-a-time in **steady-state** GAs (e.g. Whitley's Genitor).

## Theory: schemata

The **schema theorem** argues that short, low-order, above-average-fitness *schemata* (hyperplane partitions of the search space) receive exponentially increasing trials — the "building-block" / implicit-parallelism account of why GAs work. Deceptive problems, where good low-order schemata mislead, are its known limitation.

## Where GAs fit

GAs shine on **discrete, combinatorial, and mixed-integer** spaces where bit-string or permutation crossover is natural, and on large rugged landscapes. For smooth real-valued parameter tuning, the real-valued EA families — [[evolution-strategies]], [[cma-es]], [[differential-evolution]] — are usually more effective (see the empirical evidence in [[hrstka-2009-ea-comparison]]). DE is often classed in the GA family but operates directly on real vectors.

## Extensions

- **[[multimodal-optimization]]** — niching/crowding/island methods that let a GA preserve *many* optima (see [[casas-2015-ga-multimodal-review]]).
- **[[multi-objective-optimization]]** — MOEAs such as [[deb-2002-nsga-ii]] that return a Pareto front.

## See also

- [[evolution-strategies]]
- [[differential-evolution]]
- [[multimodal-optimization]]
- [[multi-objective-optimization]]
- [[darrell-whitley]]
