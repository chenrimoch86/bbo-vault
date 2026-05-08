---
title: LLVM
type: entity
tags: [compiler, framework, llvm, open-source, optimization]
created: 2026-05-08
updated: 2026-05-08
sources: [Trofin-2021-MLGO.md, MLGO-Google-Blog.md, Ashouri-2018-Compiler-Autotuning-Survey.md, RL4ReAl-2022.md, GRACE-2025.md, VeriLocc-2025.md]
---

LLVM is an open-source, modular compiler infrastructure project originally developed by Chris Lattner at UIUC. It is the dominant research and production compiler framework for C/C++/Rust and GPU compilation, and the primary platform for ML-guided [[compiler-autotuning]] research.

## Architecture Relevant to Autotuning

- **IR (Intermediate Representation)**: target-independent; optimizations (constant propagation, dead code elimination, inlining) run at this level.
- **MIR (Machine IR)**: target-specific; register allocation, instruction selection, and code generation happen here.
- **Pass pipeline**: 150+ optimization passes, each a transformation that may be applied in sequence. Pass ordering and selection are the two core autotuning problems.
- **-O2 / -O3 / -Oz**: standard optimization level presets; autotuning seeks to beat these.

## ML Integration Points

**Inlining-for-size** — replaced by a learned policy in MLGO ([[trofin-2021-mlgo]]); decisions made at each call site in the static call graph.

**Register allocation** — replaced by multi-agent RL in RL4ReAl ([[venkatakeerthy-2022-rl4real]]); MIR interference graph extracted and traversed by RL agents.

**Phase ordering / pass selection** — targeted by GRACE ([[grace-2025]]) via pass synergy graphs and contrastive program clustering.

**GPU MIR** — used by VeriLocc ([[jin-2025-verilocc]]) for cross-architecture register allocation via LLM + Z3 SMT verification.

## Infrastructure for Research

- **Compiler-Gym**: RL training environment wrapping LLVM optimization problems.
- **LLVM-gRPC**: framework proposed in MLGO for communication between RL models and the compiler during training.
- **Autophase features**: LLVM IR feature vector used for program representation in GRACE and prior RL-for-compilers work.

## See also

- [[compiler-autotuning]]
- [[google]]
