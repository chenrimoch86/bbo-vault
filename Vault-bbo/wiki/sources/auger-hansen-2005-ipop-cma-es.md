---
title: "Auger & Hansen 2005 — IPOP-CMA-ES (Restart with Increasing Population Size)"
type: source
tags: [cma-es, restart, population-size, multimodal-optimization, evolution-strategies]
created: 2026-05-23
updated: 2026-05-23
sources: [Auger-Hansen-2005-IPOP-CMA-ES.md]
---

Anne Auger and Nikolaus Hansen, *"A Restart CMA Evolution Strategy With Increasing Population Size"*, IEEE CEC 2005. Introduces **IPOP-CMA-ES**, the standard fix for the failure mode where a single [[cma-es]] run converges prematurely on a multimodal landscape.

> ⚠️ **Conversion flag.** The PDF→Markdown conversion of this source produced **no usable body** — only repeated IEEE Xplore licensing watermark lines. This page is written from the curated frontmatter description plus the well-established content of this widely cited paper. **Re-convert the PDF** (`raw/papers/Auger-Hansen-2005-IPOP-CMA-ES.md`) before relying on specific numbers or benchmark results.

## Core idea

Run CMA-ES to convergence (or a stopping criterion), then **restart** — and on each restart **double the population size λ**. Small populations behave more locally and exploitatively; large populations behave more globally and explore more broadly. Sweeping λ upward across restarts therefore shifts the search from local refinement toward global coverage automatically, without the user having to know the right population size in advance.

This is the population-size analogue of the restart logic seen elsewhere in evolutionary computation (e.g. the reannealing in [[hrstka-2009-ea-comparison]]): a cheap, robust mechanism for escaping local optima on rugged / [[multimodal-optimization|multimodal]] objectives.

## Significance

IPOP-CMA-ES was a top performer in the **CEC 2005** real-parameter optimization competition and became a long-standing baseline. The increasing-population restart scheme is now a default ingredient in production CMA-ES implementations and inspired later variants (e.g. BIPOP-CMA-ES, which interleaves large- and small-population restarts).

## See also

- [[cma-es]]
- [[evolution-strategies]]
- [[multimodal-optimization]]
- [[nikolaus-hansen]]
- [[hansen-cma-es-reference]]
