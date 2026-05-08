---
title: "RL4ReAl: Reinforcement Learning for Register Allocation (VenkataKeerthy et al., CC 2023)"
type: source
tags: [reinforcement-learning, register-allocation, llvm, compiler-autotuning, multi-agent]
created: 2026-05-08
updated: 2026-05-08
sources: [RL4ReAl-2022.md]
---

**Authors**: S. VenkataKeerthy, Siddharth Jain, Anilava Kundu, Rohit Aggarwal, Albert Cohen, Ramakrishna Upadrasta
**Venue**: CC '23 (32nd ACM SIGPLAN International Conference on Compiler Construction)
**Affiliations**: IIT Hyderabad, [[google]] (Albert Cohen)
**URL**: arxiv.org/abs/2204.02013

## Summary

RL4ReAl is the first end-to-end reinforcement learning approach to register allocation in [[llvm]]. It uses multi-agent hierarchical RL to handle the multiple interacting sub-tasks of register allocation while enforcing semantic correctness through action-space constraints. Matches or outperforms LLVM's production register allocator (LLVM-RegAlloc) on x86-64 and AArch64.

## Problem Formulation

Register allocation is reducible to graph coloring (NP-complete). Beyond graph coloring, full register allocation includes:
- **Live range splitting**: dividing a variable's live range to enable better allocation.
- **Coalescing**: merging live ranges to eliminate copy instructions.
- **Spilling**: copying a value to memory when no register is available.

These sub-tasks interact: a decision on one affects the feasibility of others.

## Methodology

**Multi-Agent Hierarchical RL**
- Separate agents model each sub-task.
- Each agent's action space is constrained to preserve semantic correctness (no two live variables share a register; register types respected).
- The interference graph is extracted from LLVM MIR; RL agents traverse it.

**MIR2Vec Embeddings**
- Proposes MIR2Vec to represent Machine IR instructions as vectors.
- Application-independent embeddings: potentially reusable for other compiler backend tasks.
- Vertices of the interference graph are MIR2Vec-encoded.

**LLVM-gRPC**
- Generic framework for communication between Python RL model and C++ LLVM compiler.
- Shared with [[trofin-2021-mlgo]] concept; enables modular ML-compiler integration.

## Results

- Targets: Intel x86-64, ARM AArch64.
- Benchmarks: SPEC CPU 2006 and SPEC CPU 2017.
- Result: **matches or outperforms LLVM's heavily-tuned production register allocator**.
- Architecture-independent: same model works across both ISAs with minimal modification.

## See also

- [[compiler-autotuning]]
- [[llvm]]
- [[jin-2025-verilocc]]
- [[trofin-2021-mlgo]]
