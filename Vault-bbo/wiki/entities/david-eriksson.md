---
title: David Eriksson
type: entity
tags: [person, researcher, bayesian-optimization, trust-region]
created: 2026-05-08
updated: 2026-05-08
sources: [Eriksson-2019-TuRBO.md]
---

David Eriksson is the lead author of TuRBO (Trust Region Bayesian Optimization, NeurIPS 2019), the paper that established local trust-region methods as the practical solution for high-dimensional BO. At time of publication he was affiliated with Cornell University; subsequently at Uber AI Labs and Meta.

## Contributions

- **TuRBO (2019)**: introduced the hyperrectangular trust region approach with adaptive expand/shrink heuristics and a Thompson-sampling multi-armed bandit for multi-TR allocation. See [[trust-region-bo]] and [[eriksson-2019-turbo]].
- TuRBO became a standard baseline and building block for subsequent HDBO work: AdaScale-TuRBO ([[adascale-turbo-2026]]), MG-TuRBO ([[mg-turbo-2026]]), REI ([[namura-2024-rei]]), and SNBO ([[koratikere-2025-snbo]]) all cite or extend it.

## See also

- [[trust-region-bo]]
- [[eriksson-2019-turbo]]
- [[high-dimensional-bo]]
