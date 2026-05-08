---
title: "LLaMEA-BO: LLM Evolutionary Algorithm for Bayesian Optimization (Li et al., 2025)"
type: source
tags: [llm, bayesian-optimization, evolutionary-algorithm, algorithm-design, metaheuristic]
created: 2026-05-08
updated: 2026-05-08
sources: [Li-2025-LLaMEA-BO.md]
---

**Authors**: Li et al.
**Year**: 2025

## Summary

LLaMEA-BO uses an LLM as the variation operator in a (µ+λ) evolution strategy where **the individuals are complete Python BO algorithm implementations**. Rather than optimizing hyperparameters within a fixed algorithm, the LLM evolves the algorithm itself — generating new acquisition functions, surrogate models, or full BO loops as Python code.

## Methodology

**Population Representation**
- Each individual in the population is a complete Python class implementing a BO algorithm.
- Individuals define: surrogate model, acquisition function, initialization strategy, and optimization loop.

**Crossover**
- Prompt: combine two parent algorithms into a single improved algorithm.
- LLM synthesizes the best elements of both parents.

**Mutation**
- Prompt: improve a single parent algorithm (identify weaknesses, propose enhancements).
- LLM reasons about algorithmic choices and suggests modifications.

**Evaluation**
- Each generated algorithm is executed on benchmark functions and scored.
- Scores form the fitness landscape for the ES selection step.

## Results

- Evaluated on the BBOB/COCO benchmark platform (standard continuous BBO benchmarks).
- Outperforms handcrafted BO baselines on 19 of 24 BBOB functions in 5D.
- Generalizes to higher-D problems and Bayesmark (real-world HPO benchmark).

## Relationship to Other LLM-BO Work

Unlike [[yang-2023-opro]] (LLM optimizes solutions), [[liu-2024-llambo]] (LLM replaces surrogate), or [[meindl-2025-gptopt]] (LLM fine-tuned as surrogate), LLaMEA-BO targets **meta-level optimization**: evolving the algorithm rather than the solution.

## See also

- [[llm-bo-hybrid]]
- [[bayesian-optimization]]
- [[hyperparameter-optimization]]
- [[yang-2023-opro]]
