---
title: Google / Google DeepMind / Google Research
type: entity
tags: [company, google, deepmind, research-lab, compiler, llm]
created: 2026-05-08
updated: 2026-05-08
sources: [Trofin-2021-MLGO.md, MLGO-Google-Blog.md, Yang-2023-OPRO.md, Wang-2018-EBO.md]
---

Google and its research divisions (Google Research, Google Brain, Google DeepMind) have produced several significant contributions relevant to this wiki, spanning ML-guided compilers, LLM-based optimization, and large-scale BO.

## Key Contributions

**MLGO — ML-Guided Compiler Optimizations** (2021–2022, Google Inc.)
- [[trofin-2021-mlgo]]: Mircea Trofin, Yundi Qian, Eugene Brevdo, Zinan Lin, Krzysztof Choromanski, David Li. First full integration of ML (policy gradient RL + evolution strategies) in a complex LLVM pass (inlining-for-size). Up to 7% code size reduction vs -Oz.
- [[mlgo-google-blog-2022]]: reports deployment on Fuchsia OS (6.3% code size reduction) and regalloc-for-performance (0.3–1.5% QPS). Framework open-sourced at `github.com/google/ml-compiler-opt`.

**OPRO — Optimization by Prompting** (2023, Google DeepMind)
- [[yang-2023-opro]]: Chengrun Yang, Xuezhi Wang, et al. LLM as optimizer: meta-prompt with solution-score history; +8% on GSM8K, +50% on BBH tasks. Foundational paper for [[llm-bo-hybrid]] paradigm.

**EBO — Ensemble Bayesian Optimization** (2018, MIT + DeepMind)
- [[wang-2018-ebo]]: Pushmeet Kohli (DeepMind) co-authored. Additive GP ensemble with Mondrian partitions; scales BO to 10K+ observations.

## See also

- [[compiler-autotuning]]
- [[llm-bo-hybrid]]
- [[bayesian-optimization]]
- [[llvm]]
