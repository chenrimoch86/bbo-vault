---
title: "Beyer & Schwefel 2002 — Evolution Strategies: A Comprehensive Introduction"
type: source
tags: [evolution-strategies, self-adaptation, evolutionary-algorithm, continuous-optimization]
created: 2026-05-23
updated: 2026-05-23
sources: [Beyer-Schwefel-2002-Evolution-Strategies-Intro.md]
---

Hans-Georg Beyer and Hans-Paul Schwefel, *"Evolution Strategies: A Comprehensive Introduction"*, Natural Computing 1:3–52, 2002. The canonical survey of the [[evolution-strategies]] (ES) branch of evolutionary computation — the family from which [[cma-es]] descends.

## History and philosophy

ES originated with students at TU Berlin (Rechenberg, Schwefel) in the 1960s, initially as rules for *physical* experimental optimization (e.g. minimizing drag of a body in a wind tunnel), not for static numerical functions. The first form was the **(1+1)-ES**: change all variables slightly at random; keep the change if it does not worsen the objective. Early theory (Rechenberg) established the **1/5 success rule** — the optimal mutation strength corresponds to a success probability of ~1/5, independent of dimension — and that convergence velocity scales inversely with the number of variables.

## The (μ/ρ +, λ) framework

The paper's unifying notation:

- **μ** — parent population size; **λ** — offspring per generation; **ρ** — number of parents recombined per offspring (mixing number; ρ=1 means no recombination).
- **Plus selection (μ+λ)** — select the μ best from parents *and* offspring; **elitist**, guarantees survival of the best. Recommended for discrete/combinatorial spaces.
- **Comma selection (μ,λ)** — select only from the λ offspring; parents are forgotten. Requires a birth surplus (μ < λ). Recommended for unbounded continuous spaces `R^N` because it escapes stagnation, at the cost of being able to diverge.

Marriage (parent selection for recombination) in ES is **random**, not fitness-biased — selection pressure comes entirely from the truncation step. This contrasts with the fitness-proportionate parent selection of the [[genetic-algorithm]].

## Self-adaptation — the central ES idea

An ES individual carries not just object parameters **y** but **endogenous strategy parameters s** (mutation strengths / step sizes) that *evolve along with the solution*. Mutation strengths are typically perturbed log-normally; selection implicitly favors individuals that happened to carry good step sizes. This online, parameter-free control of the search distribution is the conceptual seed that [[cma-es]] generalizes to a full covariance matrix (and which CSA/CMA later automated). The paper also discusses correlated mutations via rotation (up to N(N−1)/2 covariances) — the full flexibility of the Gaussian that small populations of the era could not exploit.

## See also

- [[evolution-strategies]]
- [[cma-es]] — the modern descendant; covariance generalizes ES step-size self-adaptation
- [[differential-evolution]], [[genetic-algorithm]]
- [[hans-georg-beyer]], [[hans-paul-schwefel]]
