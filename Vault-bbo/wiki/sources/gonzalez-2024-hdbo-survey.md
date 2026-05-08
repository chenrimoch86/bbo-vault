---
title: "High-Dimensional Bayesian Optimization Survey (Gonzalez et al., 2024)"
type: source
tags: [survey, high-dimensional, bayesian-optimization, benchmark, discrete-sequences]
created: 2026-05-08
updated: 2026-05-08
sources: [Gonzalez-2024-HDBO-Survey.md]
---

**Authors**: Gonzalez et al.
**Venue**: NeurIPS 2024 Datasets and Benchmarks Track
**URL**: (NeurIPS 2024)

## Summary

A systematic survey and benchmark of [[high-dimensional-bo]] methods, with particular focus on **discrete sequence optimization** (protein engineering, drug discovery). Provides a 7-category taxonomy of HDBO strategies and a unified benchmark suite (`poli`, `poli-baselines`) to enable fair comparison.

## Key Contributions

**7-Category HDBO Taxonomy**
1. **Variable selection** — identify the active dimensions; optimize only those.
2. **Additive models** — decompose f as sum of low-D components ([[wang-2018-ebo]]).
3. **Trust regions** — local GP within adaptive hyperrectangle ([[trust-region-bo]]).
4. **Linear embeddings** — project search to a learned low-D subspace (REMBO, ALEBO).
5. **Nonlinear embeddings** — VAE or other learned latent space mappings.
6. **Gradient information** — exploit available gradient oracles.
7. **Structured spaces** — kernels for sequences, graphs, molecules.

**Why GP Fails in High-D**
- GP fitting degrades above ~10D due to pairwise distance concentration.
- Acquisition function optimization becomes intractable.
- O(n³) scaling limits observation count relative to the dimension-required sample budget.

**Benchmark (`poli` / `poli-baselines`)**
- Unified framework for discrete-sequence optimization tasks.
- Covers protein engineering and drug design objectives.
- Enables reproducible comparison across the 7 strategy families.

**Domain Focus: Discrete Sequences**
- Motivates nonlinear embedding approaches (VAEs) and structured kernels.
- Most practical high-value applications (protein design, small molecule optimization) live here.

## See also

- [[high-dimensional-bo]]
- [[bayesian-optimization]]
- [[gaussian-process]]
- [[trust-region-bo]]
