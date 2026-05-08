---
title: "A Survey on Machine Learning in Compiler Optimization (Ashouri et al., 2018)"
type: source
tags: [survey, compiler-autotuning, machine-learning, phase-ordering, llvm, gcc]
created: 2026-05-08
updated: 2026-05-08
sources: [Ashouri-2018-Compiler-Autotuning-Survey.md]
---

**Authors**: Amir H. Ashouri et al.
**Venue**: ACM Computing Surveys, 2018
**Scope**: 200+ papers over 25 years of ML-guided compiler optimization

## Summary

A comprehensive survey of machine learning applied to compiler optimization, organized around the two core problems: **optimization pass selection** (which passes to apply) and **phase ordering** (the sequence). Covers the GCC and [[llvm]] ecosystems. Provides a structured taxonomy of the research landscape.

## Survey Organization

The survey organizes prior work along five dimensions:

1. **Data acquisition**: how training data is collected — iterative compilation, off-line profiling, random sampling.
2. **Preprocessing**: feature extraction from programs (static IR features, dynamic profiling, program embeddings).
3. **ML models**: decision trees, SVMs, neural networks, clustering, collaborative filtering, RL.
4. **Prediction types**: direct optimization level prediction, relative speedup ranking, performance distribution estimation.
5. **Space exploration**: how the pass/phase space is navigated — random, evolutionary, BO, RL.

## Key Domain Facts

- **GCC**: 200+ optimization passes at -O3 level.
- **LLVM**: 150+ optimization passes; modular pass pipeline facilitates ML integration.
- **Phase ordering**: the NP-hard combinatorial problem of pass sequencing; individual program characteristics determine which orderings are beneficial.
- **Benchmark suites**: SPEC CPU (2000, 2006, 2017), Polybench, cBench used across works.

## Historical Context

The survey spans 25 years (roughly 1993–2018), covering the transition from hand-engineered feature selection through supervised ML (SVM, NN) to early RL and BO approaches. It provides context for understanding why recent work (MLGO [[trofin-2021-mlgo]], GRACE [[grace-2025]], RL4ReAl [[venkatakeerthy-2022-rl4real]], VeriLocc [[jin-2025-verilocc]]) represents a maturation rather than a departure from prior approaches.

## See also

- [[compiler-autotuning]]
- [[llvm]]
- [[trofin-2021-mlgo]]
- [[grace-2025]]
