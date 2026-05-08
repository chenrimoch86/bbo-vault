---
title: "Regional Expected Improvement for Trust-Region BO (Namura, AAAI 2025)"
type: source
tags: [acquisition-function, trust-region, bayesian-optimization, expected-improvement, fujitsu]
created: 2026-05-08
updated: 2026-05-08
sources: [Namura-2024-REI.md]
---

**Authors**: Namura et al.
**Venue**: AAAI 2025
**Affiliation**: Fujitsu Research

## Summary

Proposes Regional Expected Improvement (REI), a novel [[acquisition-function]] designed specifically for [[trust-region-bo]]. REI identifies **regions** (rather than individual points) with high probability of containing the global optimum, and selects the trust region to explore next based on this criterion. Integrates directly with TuRBO ([[eriksson-2019-turbo]]).

## Methodology

**Regional Probability of Optimality**
- For each candidate trust region centered at a point, compute the probability that the global optimum lies within that region, given the current GP posterior.
- This is a regional variant of the classical EI computation.

**Theoretical Guarantee**
- REI provides a theoretical proof that the selected trust region is optimal in the sense of maximizing the probability of containing the global optimum.
- This is the first TR-BO method with such a formal selection guarantee.

**No Problem-Structure Assumptions**
- Works without assuming additivity, low intrinsic dimensionality, or other structural properties of the objective.
- Addresses local optima stagnation generically.

## Integration with TuRBO

REI replaces the TR allocation component of TuRBO. Instead of a Thompson-sampling multi-armed bandit, REI uses its regional probability criterion to determine which TR (or restart center) to activate next.

## Relevance

Fujitsu's interest in HDBO likely stems from industrial optimization applications. REI provides a principled alternative to heuristic TR selection rules.

## See also

- [[acquisition-function]]
- [[trust-region-bo]]
- [[bayesian-optimization]]
- [[eriksson-2019-turbo]]
