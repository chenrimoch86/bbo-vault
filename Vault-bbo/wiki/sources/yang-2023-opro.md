---
title: "OPRO: Large Language Models as Optimizers (Yang et al., 2023)"
type: source
tags: [llm, optimization, prompt-optimization, meta-prompt, google-deepmind]
created: 2026-05-08
updated: 2026-05-08
sources: [Yang-2023-OPRO.md]
---

**Authors**: Chengrun Yang*, Xuezhi Wang, Yifeng Lu, Hanxiao Liu, Quoc V. Le, Denny Zhou, Xinyun Chen*
**Venue**: ICLR 2024 (arXiv 2023)
**Affiliation**: [[google]] DeepMind (* equal contribution)
**URL**: arxiv.org/abs/2309.03409 | Code: github.com/google-deepmind/opro

## Summary

OPRO (Optimization by PROmpting) establishes LLMs as general-purpose derivative-free optimizers by encoding the optimization problem in natural language. The meta-prompt contains the history of (solution, score) pairs; the LLM generates new candidate solutions that aim to improve on prior results. No gradient information is required. Foundational paper in the [[llm-bo-hybrid]] paradigm.

## Methodology

**Meta-Prompt Structure**
1. Prior solution-score pairs: the trajectory of generated solutions and their objective values.
2. Task description: natural language specification of the optimization problem.
3. (For prompt optimization) Few-shot examples from the training set.

**Optimization Loop**
1. Generate new solutions from the meta-prompt.
2. Evaluate solutions on the objective (training accuracy, TSP tour length, etc.).
3. Add (solution, score) pairs to meta-prompt.
4. Repeat until convergence.

## Results

**Prompt Optimization (main application)**
- Optimizes instruction prompts for LLM reasoning tasks.
- Best prompt ("Take a deep breath and work on this problem step-by-step."): +8% over "Let's think step by step" on GSM8K.
- Up to +50% improvement on Big-Bench Hard movie_recommendation task.

**TSP and Linear Regression**
- LLM finds good solutions on small-scale instances through meta-prompting alone; matches hand-designed heuristics in some cases.

**Optimizer LLMs tested**: PaLM 2-L-IT, PaLM 2-L, GPT-3.5-turbo, GPT-4. All serve as effective optimizers; GPT-4-optimized prompts tend to be more verbose.

## Significance

OPRO shows that LLMs can implicitly learn optimization strategies from the trajectory of (solution, score) pairs, without any formal algorithm specification. It is the conceptual precursor to BORA ([[huo-2025-bora]]), LLINBO ([[chang-2025-llinbo]]), and LLaMEA-BO ([[li-2025-llamea-bo]]).

## See also

- [[llm-bo-hybrid]]
- [[hyperparameter-optimization]]
- [[bayesian-optimization]]
- [[google]]
