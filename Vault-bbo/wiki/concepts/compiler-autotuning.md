---
title: Compiler Autotuning
type: concept
tags: [compiler, autotuning, llvm, machine-learning, reinforcement-learning, register-allocation]
created: 2026-05-08
updated: 2026-05-08
sources: [Ashouri-2018-Compiler-Autotuning-Survey.md, Trofin-2021-MLGO.md, MLGO-Google-Blog.md, GRACE-2025.md, RL4ReAl-2022.md, VeriLocc-2025.md]
---

Compiler autotuning replaces hand-crafted compiler optimization heuristics with learned models, addressing two core problems: **pass selection** (which optimizations to apply) and **phase ordering** (the sequence in which passes run). [[llvm]] has 150+ optimization passes; GCC has 200+.

## Problem Formulations

**Pass selection** — choosing a subset of available passes for a given program. Exponential search space; program-dependent optimal choices.

**Phase ordering** — the order of passes matters because passes interact: inlining expands code that scalar replacement then simplifies, changing what later vectorization sees.

**Register allocation** — assigning unbounded virtual registers to a finite physical register set; NP-complete (reducible to graph coloring). Sub-problems: coloring, spilling, coalescing, live-range splitting.

## ML/RL Approaches

### Heuristic Replacement (MLGO)
[[trofin-2021-mlgo]] and [[mlgo-google-blog-2022]]: [[google]] replaced LLVM's inlining-for-size heuristic with a policy gradient RL + Evolution Strategies model. Up to 7% code size reduction vs. -Oz; 6.3% reduction on Fuchsia OS. Also applies to regalloc-for-performance (0.3–1.5% QPS improvement). Key framework insight: ML scales better with features and corpora than hand-written heuristics; trained models generalize across months of compiler evolution.

### Contrastive Learning + Genetic Algorithm (GRACE)
[[grace-2025]]: four-stage pipeline — (1) pass synergy graph to generate seed sequences and a pass pool; (2) contrastive learning on Autophase features → k-means clustering of programs; (3) cluster-specific GA evolution with global seeds; (4) test-time coreset evaluation + optional refinement. Results: 10.09% improvement over -Oz on LLVM 10; <1s per program at inference.

### Multi-Agent RL for Register Allocation (RL4ReAl)
[[venkatakeerthy-2022-rl4real]] (CC '23): first end-to-end RL approach to register allocation in LLVM. Multi-agent hierarchical RL handles sub-tasks (coloring, splitting, spilling, coalescing) with action-space constraints enforcing correctness. Proposes MIR2Vec embeddings for Machine IR representation. Matches/beats LLVM's production allocator on SPEC CPU 2006/17 (x86-64, AArch64).

### LLM + Formal Verification for GPU Register Allocation (VeriLocc)
[[jin-2025-verilocc]]: fine-tunes a 7B LLM to translate normalized MIR into physical register assignments (seq2seq). Static analysis normalizes MIR across architectures (80–90% token reduction). Z3 SMT solver verifies correctness; re-samples on failure. Results: 85–99% single-shot accuracy; beats rocBLAS by 11.6% on AMD MI250x GEMM kernels.

## Survey Landscape

[[ashouri-2018-compiler-autotuning-survey]] (ACM Computing Surveys, 2018) covers 200+ papers over 25 years. Organized around: data acquisition → preprocessing → ML models → prediction types → space exploration → target domain.

## Relationship to BBO

Compiler autotuning is a [[bayesian-optimization]] application domain: the objective function is program performance (code size, runtime, throughput) and is expensive to evaluate (requires compilation + benchmarking). Phase ordering is also a structured combinatorial optimization problem suited to evolutionary methods.

## See also

- [[bayesian-optimization]]
- [[surrogate-model]]
- [[llvm]]
- [[google]]
