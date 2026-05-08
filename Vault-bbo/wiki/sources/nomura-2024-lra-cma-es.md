---
title: "LRA-CMA-ES: Online Learning Rate Adaptation for CMA-ES (Nomura et al., 2024)"
type: source
tags: [cma-es, evolution-strategy, learning-rate, adaptation, noisy-optimization]
created: 2026-05-08
updated: 2026-05-08
sources: [Nomura-2024-CMA-ES-Learning-Rate.md]
---

**Authors**: Nomura et al.
**Venue**: ACM Transactions on Evolutionary Learning and Optimization, 2024

## Summary

LRA-CMA-ES adapts the covariance matrix learning rate η online during optimization. The key insight: optimal η is proportional to the signal-to-noise ratio (SNR) of the gradient estimate. LRA maintains constant SNR automatically, without requiring knowledge of the noise level or problem structure.

## Core Insight: Learning Rate ↔ SNR

In CMA-ES, the covariance matrix update uses learning rates c_1 (rank-1) and c_μ (rank-μ). These are set to default fixed values that work well on average but may be suboptimal for:
- **Multimodal problems**: many local optima → high signal at exploration phase, low signal near convergence → varying SNR.
- **Noisy problems**: noise corrupts gradient estimates → low SNR → smaller η needed.

**ODE analysis** (deterministic approximation of CMA-ES dynamics) shows that:
- Large η → fast covariance adaptation, but overshoots on noisy/multimodal landscapes.
- Small η → stable but slow adaptation.
- Optimal η ∝ SNR of the rank-1 path.

## LRA Mechanism

At each generation, LRA estimates the current SNR from the consistency of recent evolution path updates (without knowing the noise level). It adjusts η to maintain a target SNR, effectively:
- Increasing η when the gradient signal is strong and consistent.
- Decreasing η when updates are noisy or inconsistent.

## Comparison to PSA-CMA-ES

PSA-CMA-ES adapts population size (a complementary adaptation). LRA-CMA-ES adapts learning rate instead. LRA is orthogonal to PSA and can be combined.

## Limitations

LRA-CMA-ES does not address **weakly structured multimodal** problems (landscapes with many flat-ish basins). These require restart strategies (IPOP, BIPOP) rather than learning rate adaptation.

## See also

- [[cma-es]]
- [[high-dimensional-bo]]
