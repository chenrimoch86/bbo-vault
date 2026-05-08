---
title: "VeriLocc: LLM + Formal Verification for GPU Register Allocation (Jin et al., 2025)"
type: source
tags: [llm, register-allocation, gpu, formal-verification, compiler-autotuning, smt]
created: 2026-05-08
updated: 2026-05-08
sources: [VeriLocc-2025.md]
---

**Authors**: Lesheng Jin, Zhenyuan Ruan, Haohui Mai, Jingbo Shang
**Affiliations**: UC San Diego, MIT, CausalFlow Inc.
**Year**: 2025
**URL**: arxiv.org/abs/2506.17506
**Code**: github.com/Jimmy-MMMM/VeriLocc

## Summary

VeriLocc combines a fine-tuned 7B LLM with formal verification (SMT/Z3) to solve GPU register allocation as a sequence-to-sequence translation task (MIR → physical register assignments). Achieves 85–99% single-shot accuracy and near-100% pass@100 via verifier-guided resampling. Outperforms rocBLAS (AMD's expert-tuned BLAS library) by 11.6% on GEMM kernels for AMD MI250x.

## Key Challenges Addressed

1. **Context length**: GPU kernels after inlining and unrolling can exceed 50,000 tokens. VeriLocc normalizes MIR to reduce token count by 80–90%.
2. **Cross-architecture generalization**: GPU architectures differ in register file size, register bank constraints, pipeline stalls. VeriLocc uses static analysis to normalize MIR across toolchains.
3. **Correctness**: invalid register assignments silently corrupt programs. Z3 SMT solver formally verifies each allocation.

## Methodology

**MIR Normalization**
- Static analysis normalizes PTX (CUDA), LLVM MIR (ROCm), and other toolchain-specific IRs into a unified format.
- Extracts register allocation results from ISA via dataflow analysis.
- 80–90% token reduction enables practical LLM context usage.

**Seq2Seq LLM Fine-Tuning**
- 7B LLM fine-tuned to translate normalized MIR → JSON-style virtual-to-physical register mapping.
- Training data: compiler-generated outputs from multiple toolchains + expert-optimized libraries (e.g., rocBLAS assembly).
- Treats different GPU ISAs as "dialects" of a shared computational language.

**Verifier-Guided Regeneration**
- Generated mapping is encoded as an SMT problem.
- Z3 checks: (1) consistent mapping (same virtual register → same physical), (2) non-overlapping liveness (conflicting live ranges → disjoint physical registers).
- On failure: resample from LLM until a valid allocation is found.

## Results

| Task | Single-shot accuracy | pass@100 |
|---|---|---|
| GEMM (PTX/SASS) | 85–99% | ~100% |
| MHA (multi-head attention) | 85–99% | ~100% |

**GEMM kernel on AMD MI250x**: VeriLocc discovers register assignments that exploit register bank non-conflicts missed by existing compilers and human experts. Runtime **11.6% better than rocBLAS** (state-of-the-art vendor library).

## Relationship to RL4ReAl

[[venkatakeerthy-2022-rl4real]] uses multi-agent RL for CPU register allocation in [[llvm]]; VeriLocc uses LLM + formal verification for GPU register allocation. Both address the NP-complete allocation problem but with fundamentally different ML architectures and verification strategies.

## See also

- [[compiler-autotuning]]
- [[llvm]]
- [[venkatakeerthy-2022-rl4real]]
- [[llm-bo-hybrid]]
