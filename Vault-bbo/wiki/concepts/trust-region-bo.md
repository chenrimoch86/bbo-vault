---
title: Trust Region Bayesian Optimization
type: concept
tags: [trust-region, bayesian-optimization, high-dimensional, local-model]
created: 2026-05-08
updated: 2026-05-08
sources: [Eriksson-2019-TuRBO.md, AdaScale-TuRBO-2026.md, MG-TuRBO-2026.md, Namura-2024-REI.md]
---

Trust Region Bayesian Optimization (TR-BO) restricts GP surrogate fitting and acquisition optimization to a local hyperrectangular region around the current best (incumbent), avoiding the curse of dimensionality that degrades global BO above ~20D.

## Core Idea

Instead of fitting one GP to all observations across the full domain, TR-BO maintains a **trust region** (TR) — a hyperrectangle of side length L centered on the incumbent. The GP is fitted only on points within (or near) this region; the acquisition function is optimized only inside it.

The TR adapts based on optimization progress:
- **Successes** (new incumbent found): expand the TR (double L).
- **Failures**: shrink the TR (halve L).
- **Restart**: when L < L_min, reset with a new random center (or guided restart).

## TuRBO (Eriksson et al., NeurIPS 2019)

[[eriksson-2019-turbo]] is the canonical TR-BO algorithm. Key design choices:
- τ_succ = 3, τ_fail = ⌈d/q⌉ (d = dimension, q = batch size)
- L_init = 0.8, L_min = 2⁻⁷, L_max = 1.6 (normalized domain [0,1]^d)
- **Multiple trust regions** run in parallel; a Thompson-sampling multi-armed bandit allocates evaluations across TRs.
- Outperforms CMA-ES, EBO, BOHAMIANN on 14D–200D benchmarks; runtime < 1 min vs. hours for global BO.

## AdaScale-TuRBO (Tang & Paulson, 2026)

[[adascale-turbo-2026]] diagnoses TuRBO's GP degeneracy in high-D: pairwise distances scale Θ(L√D), making the kernel matrix near-diagonal. Fix: scale the GP lengthscale prior by L√D using a LogNormal prior with mean μ₀ + log(L√D), estimated via MAP. Consistent wins on 50D–100D benchmarks and 60D rover trajectory planning.

## MG-TuRBO (2026)

[[mg-turbo-2026]] adds **memory-guided restarts**: clusters prior evaluations into basins in the normalized design space, then selects restart centers from basins that are promising (high quality) but underexplored (low visitation count). Demonstrated on 14D and 84D traffic simulation calibration problems.

## REI Acquisition for Trust Regions

[[namura-2024-rei]] proposes the Regional Expected Improvement [[acquisition-function]], which selects the trust region most likely to contain the global optimum, with theoretical guarantees. Addresses stagnation without problem-structure assumptions.

## Strengths and Limitations

- **Strengths**: practical on 20D–200D; avoids GP degeneracy; fast per-iteration; no global acquisition optimization needed.
- **Limitations**: multiple restarts lose global exploration; TR sizing heuristics may be suboptimal; GP still degrades without lengthscale correction (cf. AdaScale).

## See also

- [[bayesian-optimization]]
- [[gaussian-process]]
- [[acquisition-function]]
- [[high-dimensional-bo]]
- [[cma-es]]
