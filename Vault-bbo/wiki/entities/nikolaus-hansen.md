---
title: Nikolaus Hansen
type: entity
tags: [person, researcher, evolution-strategy, cma-es]
created: 2026-05-08
updated: 2026-05-08
sources: [CMA-ES-homepage.md, VenkatRamanan-LM-MA-ES.md]
---

Nikolaus Hansen is the primary creator of the Covariance Matrix Adaptation Evolution Strategy (CMA-ES), the leading second-order gradient-free optimization algorithm for continuous black-box problems. He has been affiliated with INRIA (France) and the Universite Paris-Saclay, following earlier work at TU Berlin and ETH Zurich.

## Contributions

- **CMA-ES (1996–present)**: designed the core algorithm, successive refinements (rank-μ update, rank-1 update with cumulative path, negative weights, step-size adaptation via CSA), and the reference Python implementation (`pycma`). See [[cma-es]].
- **Reference implementation**: maintains `cma-es.github.io` and the `pycma` package, which serves as the canonical source for algorithm parameters and variants; summarized in [[hansen-cma-es-reference]].
- His theoretical framing of CMA-ES as approximate natural gradient descent (information geometry connection) influenced subsequent work including MA-ES and LM-MA-ES ([[loshchilov-2017-lm-ma-es]]).

## See also

- [[cma-es]]
- [[hansen-cma-es-reference]]
- [[loshchilov-2017-lm-ma-es]]
