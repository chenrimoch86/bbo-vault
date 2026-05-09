---
title: "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models (Wei et al., 2022)"
type: source
tags: [chain-of-thought, prompting, llm, reasoning, few-shot]
created: 2026-05-10
updated: 2026-05-10
sources: [Wei-2022-Chain-of-Thought.md]
---

**Authors**: Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Brian Ichter, Fei Xia, Ed Chi, Quoc Le, Denny Zhou (Google Research, Brain Team)
**Year**: 2022
**Venue**: NeurIPS 2022
**URL**: arxiv.org/pdf/2201.11903

## Summary

Chain-of-Thought (CoT) prompting elicits multi-step reasoning from large language models by including intermediate reasoning steps as exemplars in few-shot prompts. Rather than training or fine-tuning, CoT emerges from prompt structure alone in sufficiently large models (≥100B parameters). Demonstrates state-of-the-art performance on GSM8K math word problems with PaLM 540B, surpassing fine-tuned models. Foundational for any LLM-based structured extraction task.

## Core Method

Standard few-shot prompting: `⟨question, answer⟩` exemplars.
Chain-of-thought prompting: `⟨question, reasoning steps, answer⟩` exemplars.

```
Standard:
Q: cafeteria had 23 apples, used 20, bought 6 more. How many?
A: The answer is 27.  ← wrong

Chain-of-thought:
Q: cafeteria had 23 apples, used 20, bought 6 more. How many?
A: Started with 23. Used 20: 23-20=3. Bought 6 more: 3+6=9. The answer is 9.  ← correct
```

## Key Findings

- CoT helps arithmetic, commonsense, and symbolic reasoning tasks
- **Emergent behavior**: CoT only works for models ≥ ~100B parameters; smaller models show no improvement or degradation
- Only 8 few-shot exemplars needed (no large dataset)
- Works with greedy decoding; majority voting over multiple samples further improves results

## Relevance to ISP C++ Analysis

The [[cpp-register-profiling-workflow]] requires LLMs to extract structured information from ISP C++ source code:
- Register names, ranges (min/max), default values
- Dead zones (values that produce no output change)
- Conditional thresholds

CoT prompting is the right approach here: provide the model with exemplar extractions (a few manually done blocks), ask it to show its reasoning step by step, then give the answer. This:
- Reduces hallucination by forcing intermediate reasoning to be explicit
- Makes errors detectable (wrong reasoning chain visible)
- Allows few-shot examples from different ISP blocks to generalize across the codebase

**Example CoT prompt for register extraction**:
```
Here is how I analyze an ISP block to extract register profiles:

[Block 1 C++ code]
Reasoning: Line 42 clamps output to [0, 255]. Line 18 uses reg_sharp_gain as a multiplier.
  When reg_sharp_gain=0, the sharpening term is zero (dead zone). Max useful value
  appears at line 56 where saturation clamp triggers...
Result: reg_sharp_gain: range=[0,127], dead_zone=[0,1], effective=[2,127]

Now analyze this block:
[Block N C++ code]
```

## See also

- [[llm-bo-hybrid]]
- [[cpp-register-profiling-workflow]]
- [[roziere-2023-code-llama]]
- [[hou-2023-llms-for-se]]
