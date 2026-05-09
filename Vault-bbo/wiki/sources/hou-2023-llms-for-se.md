---
title: "Large Language Models for Software Engineering: A Systematic Literature Review (Hou et al., 2023)"
type: source
tags: [llm, software-engineering, code-understanding, survey, information-extraction]
created: 2026-05-10
updated: 2026-05-10
sources: [Hou-2023-LLMs-for-SE.md]
---

**Authors**: Xinyi Hou, Yanjie Zhao, Yue Liu, et al. (Huazhong University of Science and Technology, Monash, SMU)
**Year**: 2023 (ACM TOSEM 2024)
**URL**: arxiv.org/pdf/2308.10620

## Summary

Systematic literature review of 395 papers (2017–2024) on LLMs for Software Engineering. Categorizes LLMs used in SE, data processing approaches, optimization strategies, and a taxonomy of 85 specific SE tasks across six core activities. Maps what LLMs can and cannot reliably do on source code — directly relevant to deciding which parts of the ISP C++ analysis workflow to trust to LLMs.

## LLM Taxonomy for SE (from the survey)

**Code LLMs** (fine-tuned on code): CodeBERT, CodeT5, StarCoder, Code Llama, Codex
**General LLMs** (instruction-tuned): GPT-4, ChatGPT, LLaMA, Vicuna

Key finding: code-specialized LLMs outperform general LLMs on most SE tasks, but GPT-4 remains competitive despite not being code-specialized.

## Six SE Activity Categories

| Activity | LLM Tasks | ISP Relevance |
|----------|-----------|---------------|
| Requirements engineering | Extraction, classification, traceability | Low |
| Software design | API summarization, architecture recovery | Low |
| **Software development** | Code understanding, summarization, generation | **High** |
| Software quality assurance | Bug detection, test generation | Medium |
| **Software maintenance** | Code search, information extraction, documentation | **High** |
| Software management | Effort estimation | Low |

## What LLMs Do Well on Code (relevant to ISP workflow)

- **Code summarization**: explaining what a function does — reliable across all model sizes
- **Information extraction from code**: identifying variable names, types, ranges — reliable with CoT prompting ([[wei-2022-chain-of-thought]])
- **Code search**: finding where specific registers or functions are defined — strong with embedding-based search
- **Comment generation**: generating inline documentation for register semantics

## What LLMs Struggle With

- **Precise numeric range inference** without explicit clamp/saturation code — prone to hallucination
- **Long-range dependency tracking** across many functions (>16k tokens)
- **Deterministic behavior**: same prompt may produce different ranges on different runs

## Implications for ISP Register Profiling

The [[cpp-register-profiling-workflow]] relies on LLMs for ISP block analysis. Based on this survey's findings:
- **Trust with verification**: LLM-extracted ranges should be validated against unit tests or boundary condition checking
- **Batch multiple runs**: run extraction 3x and take the majority/intersection to reduce hallucination
- **Use CoT prompting**: forces explicit reasoning, making errors visible and correctable

## See also

- [[roziere-2023-code-llama]]
- [[wei-2022-chain-of-thought]]
- [[cpp-register-profiling-workflow]]
- [[llm-bo-hybrid]]
