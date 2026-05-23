---
title: Multimodal Optimization (Niching)
type: concept
tags: [multimodal-optimization, niching, crowding, fitness-sharing, diversity, genetic-algorithm]
created: 2026-05-23
updated: 2026-05-23
sources: [Casas-2015-GA-Multimodal-Review.md]
---

Multimodal optimization is the problem of finding **multiple optima of a single objective** — and preserving them — rather than converging onto one. The goal is a *set* of distinct high-quality solutions. The reference survey is [[casas-2015-ga-multimodal-review]].

**Not the same as multi-objective optimization.** Multimodal = one objective, many peaks; multi-objective = many objectives, a Pareto trade-off (see [[multi-objective-optimization]]). They share machinery (crowding/sharing appear in both), and a single-objective multimodal problem can be recast as a bi-objective one solved by a MOEA like [[deb-2002-nsga-ii]].

## Technique families

**Implicit diversity — structured populations.** Constrain dynamics so subpopulations form:
- **Island / coarse-grained models** — independent demes with periodic *migration*; naturally parallel.
- **Diffusion / cellular GAs** — grid-local mating so neighborhoods self-organize into niches.

**Explicit diversity — measure and disperse crowding:**
- **Fitness sharing** — divide an individual's fitness among neighbors within radius `σ_share`; crowded areas become unattractive. Sensitive to `σ_share`.
- **Clearing** — keep only the dominant individual(s) per subpopulation; zero the rest.
- **Crowding** — offspring replace genotypically similar parents; **Deterministic** and **Probabilistic Crowding** are the refined forms.

## Practical guidance

Per the survey, **crowding** has the broadest community support for general effectiveness. Structured-population methods can underperform a plain (panmictic) [[genetic-algorithm]] for hard-to-diagnose reasons, and most methods need careful tuning — selection remains empirical.

## See also

- [[genetic-algorithm]]
- [[multi-objective-optimization]]
- [[deb-2002-nsga-ii]]
- [[casas-2015-ga-multimodal-review]]
