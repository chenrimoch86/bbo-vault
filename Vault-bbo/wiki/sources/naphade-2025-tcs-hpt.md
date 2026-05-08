---
title: "Small LLMs with Expert Blocks for Hyperparameter Tuning (TCS, IIT Roorkee, 2025)"
type: source
tags: [llm, hyperparameter-optimization, small-llm, expert-block, tcs]
created: 2026-05-08
updated: 2026-05-08
sources: [TCS-2025-Small-LLMs-HPT.md]
---

**Authors**: Om Naphade*, Saksham Bansal*, Parikshit Pareek (IIT Roorkee)
**Year**: 2025 (preprint)
**URL**: arxiv.org/abs/2509.15561
**Code**: github.com/PSquare-Lab/LLM-TCS-HPT

## Summary

Demonstrates that small, locally-run LLMs can match GPT-4 performance on [[hyperparameter-optimization]] tasks when equipped with a deterministic **Trajectory Context Summarizer (TCS)** expert block. The TCS preprocesses raw training logs into a structured, compact state report that reduces the reasoning burden on small LLMs.

## Architecture

**Trajectory Context Summarizer (TCS)**
- A deterministic (not learned) preprocessing block.
- Inputs: current trial hyperparameters, per-epoch training results, aggregated history of prior runs.
- Outputs a structured state report: current status, latest experiment summary, per-parameter history, comparative effect of recent hyperparameter changes.
- Reduces token usage and eliminates noisy/redundant signal, enabling small LLMs to reason reliably about optimization progress.

**Optimizer Agent**
- Small LLM (phi4:reasoning 14B or qwen2.5-coder 32B) receives the TCS report.
- Proposes next hyperparameter configuration via structured prompt with explicit reasoning steps.

**Analyzer Agent**
- Breaks the reasoning process into clear sub-steps; guides the LLM to produce a task-specific analysis before proposing new hyperparameters.

## Results

- Within **0.9 percentage points** of GPT-4 across 6 diverse HPT tasks.
- 10-trial budget.
- Models run locally: privacy-preserving, near-zero marginal cost.

## Key Insight

Expert blocks (deterministic preprocessing) compensate for small LLMs' limited context window handling and multi-step reasoning ability. The TCS is analogous to a "gradient computation" for the LLM optimizer: it computes the structured state the LLM needs to make good decisions, offloading reasoning complexity to a reliable algorithm.

## See also

- [[llm-bo-hybrid]]
- [[hyperparameter-optimization]]
- [[huo-2025-bora]]
- [[liu-2024-llambo]]
