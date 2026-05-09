---
title: "A Fast and Elitist Multiobjective Genetic Algorithm: NSGA-II (Deb et al., 2002)"
type: source
tags: [multi-objective, nsga-ii, pareto, genetic-algorithm, evolutionary-computation]
created: 2026-05-10
updated: 2026-05-10
sources: [Deb-2002-NSGA-II.md]
---

**Authors**: Kalyanmoy Deb, Amrit Pratap, Sameer Agarwal, T. Meyarivan
**Year**: 2002
**Venue**: IEEE Transactions on Evolutionary Computation, Vol. 6, No. 2
**URL**: sci2s.ugr.es/sites/default/files/files/Teaching/OtherPostGraduateCourses/Metaheuristicas/Deb_NSGAII.pdf

## Summary

NSGA-II (Nondominated Sorting Genetic Algorithm II) is the standard multi-objective evolutionary optimizer. It improves over NSGA-I by introducing fast O(MN²) nondominated sorting, elitist selection (parent+offspring pool), and crowding distance as a parameter-free diversity mechanism. The result: better convergence to the true Pareto front, better spread of solutions, and no user-tuned sharing parameter.

## Core Algorithm

Each generation:
1. **Generate offspring** via crossover and mutation (standard GA operators)
2. **Combine** parent and offspring populations (size 2N)
3. **Fast nondominated sort** on the combined pool:
   - Front 1: solutions not dominated by any other
   - Front 2: solutions dominated only by Front 1
   - ...
4. **Select next generation**: fill N slots from Front 1, Front 2, ... in order
5. **Crowding distance tiebreaker**: when a front is partially admitted, prefer solutions with larger crowding distance (less crowded region of objective space)

**Complexity**: O(MN²) per generation (M objectives, N population), vs. O(MN³) for NSGA-I.

## Pareto Front and Crowding Distance

The Pareto front is the set of solutions that cannot be improved on one objective without worsening another. For ISP with three metrics (maximize MTF, minimize false color, minimize desaturation), the Pareto front shows all achievable trade-off combinations.

Crowding distance preserves diversity without a user-tuned sharing radius: it estimates the perimeter of the cuboid enclosing a solution's nearest neighbors in objective space. Solutions on the extremes of each objective always get infinite crowding distance (always preserved).

## Relevance to ISP Register Optimization

The current ISP optimizer uses a weighted sum of IQ metrics, committing to fixed trade-offs in advance. NSGA-II instead returns the **full Pareto front** — the complete set of Pareto-optimal register configurations — letting the engineer choose trade-offs after seeing results.

**When to use NSGA-II**:
- Exploration: map the full MTF vs. false color vs. desaturation trade-off surface
- Multiple product variants with different IQ priorities (sports, portrait, video)
- When the optimal weight vector is unknown

**Limitation**: NSGA-II is a GA, inheriting GA's weakness on continuous landscapes (no correlation memory, axis-aligned mutation). [[daulton-2020-qehvi]] is the BO alternative that scales better to expensive evaluations.

## See also

- [[multi-objective-optimization]]
- [[daulton-2020-qehvi]]
- [[cma-es]]
- [[isp-register-optimization]]
- [[Problem_Definition]]
