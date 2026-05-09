---
title: "Code Llama: Open Foundation Models for Code (Rozière et al., 2023)"
type: source
tags: [code-llm, llm, code-understanding, meta, c-plus-plus, infilling]
created: 2026-05-10
updated: 2026-05-10
sources: [Roziere-2023-CodeLlama.md]
---

**Authors**: Baptiste Rozière, Jonas Gehring, Fabian Gloeckle, et al. (Meta AI)
**Year**: 2023
**URL**: arxiv.org/pdf/2308.12950

## Summary

Code Llama is Meta's family of code-specialized LLMs fine-tuned from Llama 2. Available in 7B, 13B, 34B, and 70B sizes across three variants: foundation (Code Llama), Python-specialized (Code Llama – Python), and instruction-following (Code Llama – Instruct). Achieves state-of-the-art among open models on HumanEval (67%) and MBPP (65%). Supports 16k token context (100k for long-context inputs) and fill-in-the-middle (infilling) for all sizes ≤13B and 70B.

## Model Variants

| Variant | Best for |
|---------|---------|
| Code Llama | General code: understanding, generation, analysis |
| Code Llama – Python | Python-specific tasks |
| **Code Llama – Instruct** | Instruction following; best for "extract X from this code" tasks |

For ISP block analysis, **Code Llama – Instruct 34B** is the recommended choice: instruction-following capability + large enough for complex C++ reasoning + open weights for local deployment.

## Key Capabilities for ISP C++ Analysis

- **C++ understanding**: trained on large corpora of C/C++ code; understands pointer arithmetic, bitwise ops, struct layouts
- **16k token context**: can fit an entire ISP block implementation (~200–500 lines) in a single prompt
- **Infilling**: can complete middle sections of code given prefix and suffix — useful for annotating register ranges within existing code
- **Zero-shot instruction following**: "List all registers in this function, their ranges, and any saturation/clamping conditions" works without fine-tuning

## Comparison to General LLMs for C++ Tasks

| Model | C++ capability | Context | Cost | Open? |
|-------|---------------|---------|------|-------|
| GPT-4 | Strong | 128k | API cost | No |
| **Code Llama 34B – Instruct** | Strong (code-specialized) | 16k | Local GPU | Yes |
| Llama 2 70B | Moderate | 4k | Local GPU | Yes |
| Code Llama 7B | Basic | 16k | Local CPU | Yes |

Code Llama outperforms Llama 2 70B on code tasks while being smaller. For the ISP register extraction workflow, Code Llama 34B Instruct is more cost-effective than GPT-4 API and deployable on-premise (important for proprietary ISP source code).

## See also

- [[hou-2023-llms-for-se]]
- [[wei-2022-chain-of-thought]]
- [[cpp-register-profiling-workflow]]
- [[llm-bo-hybrid]]
