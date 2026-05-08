---
title: "LLAMBO: Large Language Models to Enhance Bayesian Optimization (Liu et al., 2024)"
type: source
tags: [llm, bayesian-optimization, surrogate, hyperparameter-optimization, warmstarting]
created: 2026-05-08
updated: 2026-05-08
sources: [Liu-2024-LLAMBO.md]
---

**Authors**: Liu et al.
**Venue**: ICLR 2024
**URL**: (ICLR 2024)

## Summary

LLAMBO integrates LLMs into [[bayesian-optimization]] as a modular, drop-in enhancement. Three independent components — zero-shot warmstarting, LLM-as-surrogate, and LLM candidate sampling — each target a distinct phase of the BO loop. The system frames the optimization state in natural language, allowing LLMs to apply domain knowledge without task-specific fine-tuning.

## Three Components

**Zero-Shot Warmstarting**
- Before any evaluations, the LLM proposes promising initial configurations based on the natural-language task description.
- Replaces random or space-filling initialization; injects prior knowledge into the optimization start.

**LLM as Surrogate**
- Given a few-shot history of (configuration, performance) pairs in natural language, the LLM predicts f(h) for new configurations.
- Replaces the [[gaussian-process]] surrogate in the sparse-data regime where GP has insufficient data.

**LLM Candidate Sampling**
- LLM generates candidate configurations directly, conditioned on the optimization history.
- Replaces acquisition function maximization over a GP surrogate.

## Strengths

- **Modular**: each component can be used independently or combined.
- **Strong early performance**: when observations are sparse (< ~20 trials), LLM knowledge dominates over GP's data-driven learning.
- **Zero fine-tuning**: works with off-the-shelf LLMs via prompting.

## Limitations

- LLM surrogate quality degrades as data accumulates (GP becomes more accurate). [[chang-2025-llinbo]] addresses this directly.
- Limited to tabular hyperparameter spaces; less suited to continuous, high-D domains.

## See also

- [[llm-bo-hybrid]]
- [[hyperparameter-optimization]]
- [[bayesian-optimization]]
- [[gaussian-process]]
- [[chang-2025-llinbo]]
