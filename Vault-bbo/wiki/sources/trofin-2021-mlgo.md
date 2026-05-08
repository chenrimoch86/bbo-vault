---
title: "MLGO: A Machine Learning Guided Compiler Optimizations Framework (Trofin et al., 2021)"
type: source
tags: [compiler-autotuning, llvm, reinforcement-learning, inlining, mlgo, google]
created: 2026-05-08
updated: 2026-05-08
sources: [Trofin-2021-MLGO.md]
---

**Authors**: Mircea Trofin*, Yundi Qian*, Eugene Brevdo, Zinan Lin, Krzysztof Choromanski, David Li
**Venue**: arXiv 2021 (MLSys 2022)
**Affiliation**: [[google]] Inc. (* equal contribution)
**URL**: arxiv.org/abs/2101.04808
**Code**: github.com/google/ml-compiler-opt

## Summary

MLGO is the first full integration of a machine-learned policy in a complex, production-grade compiler pass in [[llvm]]. It replaces the hand-crafted inlining-for-size heuristic with a model trained via policy gradient RL and Evolution Strategies (ES). Up to 7% code size reduction vs -Oz. The framework separates policy training from compiler usage, enabling offline training at scale.

## Framework Design

**Separation of concerns**: day-to-day compilation uses the embedded trained model unchanged; training happens offline on a large, representative corpus of LLVM IR modules. The compiler logs features and decisions during training; logs feed back to the RL/ES algorithm.

**gRPC interface (LLVM-gRPC)**: allows communication between the Python RL training loop and the C++ LLVM compiler. Enables non-invasive integration without modifying core compiler logic. Generalizable to other optimization passes.

**Policy gradient (REINFORCE)**: treats each inlining decision as an action, compilation outcome (size reduction) as the reward signal.

**Evolution Strategies (ES)**: used as an alternative to policy gradient; competitive and provides natural gradient direction.

## Inlining-for-Size Problem

- LLVM inliner processes a strongly-connected component (SCC) of the call graph bottom-up.
- Decision: whether to inline a specific call site.
- Feature vector: 25+ IR-level features per call site.
- Ground truth is undefined (NP-hard to determine optimal); RL's trial-and-error is a natural fit.

## Results

- Up to **7% code size reduction** vs -Oz (the most aggressive size optimization preset).
- Trained model generalizes across: diverse real-world targets, and the same targets after months of active compiler development.
- See [[mlgo-google-blog-2022]] for deployment results.

## Significance

First production-deployed ML-guided compiler pass. Demonstrates that ML models can match the generalization requirement of industrial compilers (months of evolution, diverse codebases).

## See also

- [[compiler-autotuning]]
- [[llvm]]
- [[google]]
- [[mlgo-google-blog-2022]]
- [[venkatakeerthy-2022-rl4real]]
