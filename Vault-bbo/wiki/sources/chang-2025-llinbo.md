---
title: "LLINBO: LLM-in-the-Loop Bayesian Optimization (Chang et al., 2025)"
type: source
tags: [llm, bayesian-optimization, federated-learning, theoretical-guarantees, adaptive]
created: 2026-05-08
updated: 2026-05-08
sources: [Chang-2025-LLINBO.md]
---

**Authors**: Chang et al.
**Affiliation**: University of Michigan
**Year**: 2025

## Summary

LLINBO (LLM-in-the-Loop BO) addresses a key insight about [[llm-bo-hybrid]] methods: **LLMs degrade relative to [[gaussian-process]] surrogates as observations accumulate**. Inspired by federated learning's weighted aggregation, LLINBO provides three mechanisms that progressively reduce LLM influence as data accumulates.

## Core Insight

In early optimization, LLM prior knowledge is valuable because the GP has few observations and high uncertainty. As data accumulates, the GP becomes more accurate and the LLM's suggestions (based on pre-trained knowledge rather than observed data) become less reliable. Standard LLM-BO hybrids fail to account for this dynamic.

## Three Mechanisms

**LLINBO-Transient**
- Gradually reduces the LLM's weight in the acquisition decision as a function of iteration count.
- Simple scheduled decay: LLM weight w(t) → 0 as t → ∞.

**LLINBO-Justify**
- At each step, the LLM must justify its suggestion against the current GP posterior.
- If the LLM's proposed point has low GP posterior value, it is rejected or down-weighted.
- Creates a data-driven filter on LLM suggestions.

**LLINBO-Constrained**
- LLM suggestions are constrained to lie within the GP UCB (Upper Confidence Bound) high-confidence region.
- Ensures LLM can only propose points that the GP considers plausible improvements.

## Theoretical Guarantees

LLINBO provides formal convergence and regret guarantees for the three mechanisms, grounding the adaptive weighting in theory. This is a distinguishing feature compared to most [[llm-bo-hybrid]] methods.

## Application

Validated on 3D printing hyperparameter optimization, demonstrating practical utility in manufacturing-adjacent domains where LLM prior knowledge about printing parameters exists.

## See also

- [[llm-bo-hybrid]]
- [[bayesian-optimization]]
- [[gaussian-process]]
- [[liu-2024-llambo]]
- [[hyperparameter-optimization]]
