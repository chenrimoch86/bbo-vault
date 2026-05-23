---
title: "Storn & Price 1997 — Differential Evolution"
type: source
tags: [differential-evolution, evolutionary-algorithm, global-optimization, continuous-optimization]
created: 2026-05-23
updated: 2026-05-23
sources: [Storn-Price-1997-Differential-Evolution.md]
---

Rainer Storn and Kenneth Price, *"Differential Evolution — A Simple and Efficient Heuristic for Global Optimization over Continuous Spaces"*, Journal of Global Optimization 11:341–359, 1997. The paper that introduced [[differential-evolution]] (DE), now one of the most widely used population-based methods for real-valued global optimization.

## Core idea

DE maintains a population of `NP` D-dimensional real vectors. Its defining move is the **differential mutation**: for each target vector it forms a mutant by adding a *scaled difference of two other randomly chosen population vectors* to a third:

```
v = x_r1 + F · (x_r2 − x_r3)
```

This self-scaling perturbation — the difference vector shrinks automatically as the population converges — is what distinguishes DE from [[evolution-strategies]], which draw mutations from a predetermined (Gaussian) distribution. Mutation is followed by binomial **crossover** (rate `CR`) with the target, then **greedy selection**: the trial replaces the target only if its cost is lower.

## Variants and notation

DE schemes are named `DE/x/y/z` (base vector / number of difference vectors / crossover type). The baseline used throughout the paper is **`DE/rand/1/bin`**; `DE/best/2/bin` is also highlighted as strong when `NP` is large.

## Control parameters (the paper's rules of thumb)

- `NP` ≈ 5·D to 10·D, minimum 4.
- `F` ≈ 0.5 to start; values < 0.4 or > 1 rarely help. Increase `F`/`NP` on premature convergence.
- `CR` ≈ 0.1 as a robust default; try 0.9–1.0 for faster convergence on separable problems.

Few, robust, easy-to-choose parameters are cited as DE's main practical asset; the search engine is ~20 lines of C.

## Results

On De Jong's suite plus harder multimodal/constrained functions, DE beat Adaptive Simulated Annealing (ASA), Annealed Nelder–Mead (ANM), the Breeder GA (BGA), and the EASY evolution strategy in function-evaluation count on the large majority of test cases — placing fastest among evolutionary entries at the 1st ICEO competition. The authors note an open question (later borne out by others): DE's scaling and behavior on large real-world problems was untested in 1997.

## See also

- [[differential-evolution]]
- [[hrstka-2009-ea-comparison]] — independent benchmark; finds DE robust at moderate D but degrading past ~30D
- [[evolution-strategies]]
- [[genetic-algorithm]]
- [[rainer-storn]], [[kenneth-price]]
