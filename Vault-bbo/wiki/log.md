# Wiki Log

Append-only chronological record of all wiki operations.
Grep pattern for entries: `grep "^## \[" wiki/log.md`

---

## [2026-05-08] analysis | C++ ISP Register Profiling Workflow (updated — honest split)

- Analysis page: wiki/analyses/cpp-register-profiling-workflow.md
- Updated: honest split between what LLM can find (explicit patterns) vs what needs simulator (math/cross-block)
- LLM reliable for: clamps, dead zones, categoricals, dead registers, dependencies, thresholds
- Simulator needed for: mathematical saturation, quantization, cross-block constraints, downstream clamping
- Added targeted 3-point sweep protocol for low-confidence registers

- Analysis page: wiki/analyses/cpp-register-profiling-workflow.md
- Workflow: LLM analyzes each C++ ISP block file → extracts register profiles → feeds into CMA-ES with tight bounds
- Extracts: effective ranges, dead zones, thresholds, categoricals, dead registers, conditional dependencies
- Complementary to XGBoost feature importance: structural knowledge vs empirical knowledge
- index.md updated

---

## [2026-05-08] analysis | Problem Definition — ISP Register Optimization

- Analysis page: wiki/analyses/Problem_Definition.md
- Full problem definition: system, pipeline, simulator, current approach, weak points, assets, recommendation
- index.md updated

---

## [2026-05-08] analysis | ISP Register Optimization — Final Recommendation

- Analysis page: wiki/analyses/isp-register-optimization.md
- Full revision based on: 300k XGBoost surrogate, GA optimizer, 300 runs/min simulator, real hardware as true constraint
- Final recommendation: XGBoost feature importance → active subspace → multi-start CMA-ES → simulator validation loop → real hardware top-3
- MG-TuRBO/GP-based BO ruled out: wrong regime for 300/min throughput
- LLM-BO hybrids ruled out: wrong regime for 300k training data

- Question: which BBO method suits ~200 ISP registers → image quality optimization?
- Analysis page: wiki/analyses/isp-register-optimization.md
- Updated with: expensive eval + unknown register-metric relationships constraints
- Recommendation: Phase 1 sensitivity screening (free, use existing data) → Phase 2 MG-TuRBO on active subspace (~20-40 registers)
- EBO as upgrade if sensitivity reveals disjoint register groups
- LLM-BO hybrids ruled out for this problem type

---

## [2026-05-08] query | LLM–BO Integration Patterns

- Question: which methods combine LLMs with BO and how do they improve it?
- Analysis page: wiki/analyses/llm-bo-integration-patterns.md
- Sources drawn: OPRO, LLAMBO, GPTOpt, BORA, LLINBO, LLaMEA-BO, TCS
- index.md updated

---

## [2026-05-08] analysis | Mermaid Diagram Demo

- Analysis page: wiki/analyses/mermaid-diagram-demo.md
- Diagrams: BO core loop (flowchart), LLM-BO taxonomy (flowchart), BORA switching (state diagram), concept map, TR-BO timeline, LLM trade-off quadrant
- index.md updated

---

## [2026-05-08] ingest | Batch ingest — 26 BBO/compiler/LLM sources

- Sources created (26):
  [[bartz-beielstein-2016-surrogate-bbo]], [[wang-2018-ebo]], [[gonzalez-2024-hdbo-survey]],
  [[eriksson-2019-turbo]], [[adascale-turbo-2026]], [[mg-turbo-2026]], [[namura-2024-rei]],
  [[anahideh-2019-hdbbo-uncertainty]], [[koratikere-2025-snbo]], [[hansen-cma-es-reference]],
  [[loshchilov-2017-lm-ma-es]], [[nomura-2024-lra-cma-es]], [[yang-2023-opro]],
  [[liu-2024-llambo]], [[chang-2025-llinbo]], [[meindl-2025-gptopt]], [[li-2025-llamea-bo]],
  [[huo-2025-bora]], [[naphade-2025-tcs-hpt]], [[wang-2025-llm-hpo-uav]],
  [[ashouri-2018-compiler-autotuning-survey]], [[trofin-2021-mlgo]], [[mlgo-google-blog-2022]],
  [[venkatakeerthy-2022-rl4real]], [[grace-2025]], [[jin-2025-verilocc]]
- Entities created (4): [[nikolaus-hansen]], [[david-eriksson]], [[google]], [[llvm]]
- Concepts created (10): [[bayesian-optimization]], [[gaussian-process]], [[acquisition-function]],
  [[trust-region-bo]], [[cma-es]], [[high-dimensional-bo]], [[surrogate-model]],
  [[llm-bo-hybrid]], [[compiler-autotuning]], [[hyperparameter-optimization]]
- index.md updated: 26 sources, 4 entities, 10 concepts added

---

## [2026-05-08] ingest | LLM Wiki — The Core Idea

- Summary page: wiki/sources/llm-wiki-idea.md
- Entities created: [[vannevar-bush]]
- Concepts created: [[memex]], [[rag]], [[compounding-knowledge]], [[schema-file]]
- index.md updated: 1 source, 1 entity, 4 concepts added

---

## [2026-05-08] init | Wiki initialized

- Created CLAUDE.md schema
- Created wiki/index.md
- Created wiki/log.md
- Directory structure established: wiki/sources/, wiki/entities/, wiki/concepts/, wiki/analyses/, raw/, assets/
