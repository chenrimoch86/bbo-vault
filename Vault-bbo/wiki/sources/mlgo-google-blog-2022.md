---
title: "ML-Guided Compiler Optimization in LLVM (Google Research Blog, 2022)"
type: source
tags: [compiler-autotuning, llvm, mlgo, google, deployment, regalloc]
created: 2026-05-08
updated: 2026-05-08
sources: [MLGO-Google-Blog.md]
---

**Publisher**: Google Research Blog
**Year**: 2022
**Affiliation**: [[google]] Research

## Summary

Reports on the MLGO framework's production deployment and extension to register allocation. Follows up on [[trofin-2021-mlgo]] with real-world deployment results and a second optimization target.

## Inlining-for-Size Deployment

- Deployed on **Fuchsia OS** (Google's embedded/mobile operating system).
- Result: **6.3% code size reduction** on Fuchsia binaries.
- Model trained on one corpus generalizes to the Fuchsia codebase, confirming the generalization property identified in the MLGO paper.
- Open-sourced: `github.com/google/ml-compiler-opt`; model embedded in [[llvm]] repository.

## Register Allocation for Performance

- Extended MLGO to **register allocation** (regalloc-for-performance).
- Target: improve instruction-level parallelism and reduce spills, improving execution throughput.
- Result: **0.3–1.5% QPS improvement** on internal Google services.
- TensorFlow models embedded via **XLA AOT** (ahead-of-time compilation), removing Python inference overhead.

## Technical Details

- Policy gradient training with XLA AOT embedding for production inference.
- Models embedded directly in the [[llvm]] compiler binary; no separate inference process needed.

## Relationship to Academic Work

Confirms that ML-guided compiler optimization is viable in a production setting — addressing concerns about: (1) generalization across codebases, (2) maintaining performance across compiler evolution, (3) integration complexity.

## See also

- [[compiler-autotuning]]
- [[llvm]]
- [[google]]
- [[trofin-2021-mlgo]]
