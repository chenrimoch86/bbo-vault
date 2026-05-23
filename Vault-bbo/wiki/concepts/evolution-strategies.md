---
title: Evolution Strategies (ES)
type: concept
tags: [evolution-strategies, self-adaptation, evolutionary-algorithm, continuous-optimization, gradient-free]
created: 2026-05-23
updated: 2026-05-23
sources: [Beyer-Schwefel-2002-Evolution-Strategies-Intro.md]
---

Evolution Strategies (ES) are a branch of evolutionary computation, founded at TU Berlin in the 1960s (Rechenberg, Schwefel), specialized for **real-valued, continuous, possibly noisy** optimization. They are gradient-free and population-based, and they are the lineage from which [[cma-es]] descends. The comprehensive reference is [[beyer-schwefel-2002-evolution-strategies]].

## Defining features

- **Mutation by Gaussian perturbation** of object variables, with the step size (mutation strength) as a first-class, *adapted* quantity.
- **Self-adaptation of strategy parameters.** Each individual carries endogenous strategy parameters (step sizes, and optionally a covariance/rotation) that evolve alongside the solution. Selection implicitly rewards individuals carrying good step sizes — search-distribution control with no external schedule.
- **Random recombination partners.** Parents for recombination are chosen at random; *all* selection pressure comes from the truncation step — unlike the fitness-biased parent selection of the [[genetic-algorithm]].

## The (μ/ρ +, λ) notation

- **μ** parents, **λ** offspring, **ρ** parents recombined per offspring.
- **(μ + λ) "plus" selection** — elitist (best survives); preferred for discrete/finite search spaces.
- **(μ, λ) "comma" selection** — parents discarded each generation, requires μ < λ; preferred for unbounded continuous `R^N` because it resists stagnation.
- Early theory: the **1/5 success rule** (optimal mutation strength ≈ 1/5 success probability) and convergence velocity scaling inversely with dimension.

## Relationship to other methods

ES → [[cma-es]]: CMA generalizes scalar step-size self-adaptation to a full covariance matrix (the search distribution's shape), with CSA automating the step size. ES and [[differential-evolution]] are sibling real-valued EA families — DE replaces Gaussian mutation with a *self-scaling difference-vector* perturbation. ES contrasts with the [[genetic-algorithm]], whose home turf is discrete/combinatorial encodings.

## See also

- [[cma-es]]
- [[differential-evolution]]
- [[genetic-algorithm]]
- [[surrogate-model]]
- [[hans-paul-schwefel]], [[hans-georg-beyer]], [[nikolaus-hansen]]
