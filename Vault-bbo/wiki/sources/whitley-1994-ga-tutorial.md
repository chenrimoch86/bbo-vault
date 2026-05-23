---
title: "Whitley 1994 — A Genetic Algorithm Tutorial"
type: source
tags: [genetic-algorithm, schema-theorem, crossover, selection, evolutionary-algorithm]
created: 2026-05-23
updated: 2026-05-23
sources: [Whitley-1994-GA-Tutorial.md]
---

Darrell Whitley, *"A Genetic Algorithm Tutorial"*, Statistics and Computing 4:65–85, 1994. The canonical primer on the [[genetic-algorithm]]: encodings, selection, crossover, and the theory (schema theorem, hyperplane sampling) that motivated the canonical GA.

> ⚠️ **Conversion flag.** The PDF→Markdown conversion of this source failed: the body is mojibake (corrupted font/glyph extraction), with only fragments — section heading "Selection / Recombination" and a crossover-illustration table — recoverable. This page is written from the curated frontmatter description plus the well-established, widely cited content of this paper. **Re-convert the PDF** (`raw/papers/Whitley-1994-GA-Tutorial.md`) before relying on specific figures or quotations.

## What the tutorial covers (canonical content)

- **The canonical GA.** Fixed-length (typically binary) string chromosomes; a generational loop of fitness-proportionate **selection**, **crossover** (recombination), and **mutation**; the distinction between the *genotype* (encoded string) and *phenotype* (decoded solution).
- **Selection operators.** Fitness-proportionate ("roulette wheel") selection and its scaling problems, motivating **rank-based** and **tournament** selection. Unlike [[evolution-strategies]], the GA biases *parent* selection by fitness.
- **Crossover operators.** One-point, two-point, and uniform crossover; the trade-off between disruption and recombination of useful substructures.
- **Schema theorem & building blocks.** Short, low-order, above-average **schemata** (hyperplanes) receive exponentially increasing trials — the "implicit parallelism" / building-block argument for *why* GAs work, and its limits (deception).
- **Steady-state GAs.** Whitley's own **Genitor** as the prototypical steady-state (one-at-a-time replacement) GA, contrasted with generational GAs.
- **Encodings.** Binary vs. real-coded (Gray coding, Hamming cliffs); where bit-string crossover fits discrete/combinatorial choices versus where real-valued methods like [[evolution-strategies]] / [[differential-evolution]] suit smooth continuous tuning.

## See also

- [[genetic-algorithm]]
- [[multimodal-optimization]]
- [[evolution-strategies]], [[differential-evolution]]
- [[darrell-whitley]]
