---
title: "Casas 2015 — Genetic Algorithms for Multimodal Optimization: A Review"
type: source
tags: [genetic-algorithm, multimodal-optimization, niching, diversity]
created: 2026-05-23
updated: 2026-05-23
sources: [Casas-2015-GA-Multimodal-Review.md]
---

Noe Casas, *"Genetic Algorithms for Multimodal Optimization: A Review"*, arXiv:1508.05342, 2015. A survey of techniques that keep a [[genetic-algorithm]] from collapsing onto a single optimum, so it can locate and preserve **many** optima at once — the topic of [[multimodal-optimization]].

The paper carefully separates **multimodal** optimization (one objective with many local optima; goal = find them all) from **multi-objective** optimization (several objectives traded off; goal = Pareto front) — see [[multi-objective-optimization]]. It declines to use the overloaded term "niching."

## Two families of techniques

**1. Structured-population GAs (implicit diversity).** Constrain population dynamics rather than measuring diversity directly:
- **Island / coarse-grained models** — separate subpopulations evolving independently, exchanging individuals via periodic *migration* (tunable topology, frequency, sync). Naturally parallel and partly algorithm-agnostic per island.
- **Spatially-dispersed / diffusion / cellular GAs** — individuals on a 2D grid mate only within a neighborhood radius, so demes self-organize.
- Exotic mating restrictions: multinational, religion-based, age-structured GAs.

**2. Diversity-enforcing techniques (explicit).** Measure crowding in genotype space and push individuals to new niches:
- **Fitness sharing** — an individual's fitness is divided among neighbors within radius `σ_share`; crowded regions become less attractive. Effective but sensitive to `σ_share`.
- **Clearing** — within each subpopulation, only the dominant individual(s) keep fitness; the rest are zeroed.
- **Crowding** — offspring replace genotypically similar parents. **Deterministic Crowding** (Mahfoud) and **Probabilistic Crowding** (Mengshoel) are the refined forms.

## Verdict

Crowding is the one approach with broad community agreement on general effectiveness; structured-population methods can underperform a plain (panmictic) GA for reasons that are hard to diagnose, and most methods require careful tuning. Method choice for a given multimodal problem remains empirical. The paper also notes Deb's trick of recasting a single-objective multimodal problem as a bi-objective one solved by a MOEA.

## See also

- [[multimodal-optimization]]
- [[genetic-algorithm]]
- [[multi-objective-optimization]]
- [[deb-2002-nsga-ii]] — the MOEA referenced for the bi-objective reformulation
