---
title: "GRACE: Compiler Autotuning via Contrastive Learning and Genetic Algorithms (2025)"
type: source
tags: [compiler-autotuning, llvm, contrastive-learning, genetic-algorithm, phase-ordering]
created: 2026-05-08
updated: 2026-05-08
sources: [GRACE-2025.md]
---

**Year**: 2025

## Summary

GRACE is a four-stage compiler autotuning framework targeting [[llvm]] pass sequence optimization. It combines a pass synergy graph for seed generation, contrastive learning for program clustering, cluster-specific genetic algorithm (GA) evolution, and a fast test-time coreset strategy. Results: 10.09% improvement over -Oz on LLVM 10, 10.19% on LLVM 18.1.6, with sub-second inference per program.

## Four-Stage Pipeline

**Stage 1: Pass Synergy Graph → Seed Sequences + Pass Pool**
- Constructs a graph where nodes are LLVM passes and edges encode synergistic interactions (pass A followed by pass B produces better results than either alone).
- Mines this graph to generate high-quality seed pass sequences and a filtered pass pool for evolution.

**Stage 2: Program Clustering via Contrastive Learning**
- Extracts Autophase features (LLVM IR feature vectors) for each training program.
- Fine-tunes a contrastive learning model to learn a program embedding space where similar programs (w.r.t. optimization response) cluster together.
- Applies k-means clustering to group programs into k clusters.

**Stage 3: Cluster-Specific GA Evolution with Global Seeds**
- Each cluster gets a dedicated GA that evolves pass sequences tailored to programs in that cluster.
- Global seeds from Stage 1 are shared across all cluster GAs; cluster-specific mutations refine locally.

**Stage 4: Test-Time Evaluation**
- For a new program: classify into nearest cluster, evaluate k coreset sequences (diverse representative sequences selected offline from cluster evolution).
- Optional refinement: derivative search (perturbation), localized GA, or Oz fallback.
- Inference time: < 1 second per program.

## Results

| Configuration | Improvement over -Oz |
|---|---|
| LLVM 10 | 10.09% |
| LLVM 18.1.6 | 10.19% |

Beats: CFSAT, Coreset-NVP, Autophase-PPO, OpenTuner, CompTuner across 7 benchmark datasets (19,603 training programs, 335 test programs).

## See also

- [[compiler-autotuning]]
- [[llvm]]
- [[ashouri-2018-compiler-autotuning-survey]]
