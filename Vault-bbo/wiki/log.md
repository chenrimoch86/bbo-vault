# Wiki Log

Append-only chronological record of all wiki operations.
Grep pattern for entries: `grep "^## \[" wiki/log.md`

---

## [2026-05-10] ingest | Batch ingestion of 15 new papers (ISP/IQ, surrogate, sensitivity, multi-objective, sampling, LLM)

- Source pages created (wiki/sources/):
  - burns-2000-slanted-edge-mtf.md — slanted-edge MTF, ISO 12233 SFR algorithm
  - chen-2016-xgboost.md — XGBoost: gradient boosting, importance types, surrogate use
  - sacks-1989-dace.md — DACE: GP surrogate + space-filling design, foundational paper
  - mckay-1979-lhs.md — Latin Hypercube Sampling, variance reduction proof
  - lundberg-2017-shap.md — SHAP: unified game-theoretic feature importance
  - lundberg-2018-treeshap.md — TreeSHAP: exact O(TLD²) SHAP for XGBoost
  - herman-2017-salib.md — SALib: Morris screening + Sobol indices Python library
  - iooss-2010-q2-metamodel-validation.md — Q2 coefficient, sequential validation design
  - deb-2002-nsga-ii.md — NSGA-II: fast elitist multi-objective GA, Pareto front
  - daulton-2020-qehvi.md — qEHVI: expected hypervolume improvement for multi-objective BO
  - constantine-2014-active-subspaces.md — active subspace dimension reduction
  - settles-2009-active-learning.md — active learning survey, QBC framework
  - wei-2022-chain-of-thought.md — Chain-of-Thought prompting, NeurIPS 2022
  - roziere-2023-code-llama.md — Code Llama: Meta's code-specialized LLM
  - hou-2023-llms-for-se.md — LLMs for SE systematic review (395 papers)
- Source page updated:
  - loshchilov-2017-lm-ma-es.md — added Loshchilov-2017-LM-MA-ES.md as second source
- Concept pages created (wiki/concepts/):
  - image-quality-metrics.md — MTF, false color, desaturation: measurement and ISP relevance
  - sensitivity-analysis.md — Morris/Sobol/TreeSHAP comparison and recommended workflow
  - multi-objective-optimization.md — Pareto front, NSGA-II vs. qEHVI vs. weighted sum
  - latin-hypercube-sampling.md — LHS construction, variance theorem, ISP data collection
  - active-learning.md — QBC framework, connection to ISP validation loop
  - metamodel-validation.md — Q2 metric, regional validation, acceptance thresholds
- index.md updated: +15 sources, +6 concepts

---

## [2026-05-10] update | Added AGENTS.md for cross-platform LLM access

- Created Vault-bbo/AGENTS.md: universal entry point for non-Claude LLMs (Codex, Copilot CLI, Gemini CLI)
- Includes: platform routing table, session start protocol, domain context summary, directory layout, page conventions, core operations, log/index formats, rules, file I/O tool mapping, key pages index
- Includes domain-specific context block so any LLM understands the ISP problem without reading all analyses

---

## [2026-05-09] update | Expanded GA vs CMA-ES comparison in isp-register-optimization

- Replaced brief table with full mechanistic explanation of why GA fails on continuous landscapes
- Added: crossover destroys correlations problem, axis-aligned mutation problem, no cross-generation memory
- Added: how CMA-ES covariance matrix learns register correlations, evolution paths remember direction, CSA adapts step size
- Updated diagram and comparison table with new dimensions
- File updated: wiki/analyses/isp-register-optimization.md

---

## [2026-05-09] update | Clarified validation vs retraining loop in isp-register-optimization

- Split "Iterative Surrogate Retraining Loop" into two explicit steps:
  - Step 1 Validation: always run top-K configs through full evaluation (ISP simulator + IQ measurement); ~20 sec; catches XGBoost inaccuracy before deploying
  - Step 2 Targeted Retraining: only triggered on disagreement; sample 2-5k configs in disagreement region, run full evaluation, retrain XGBoost; ~7-17 min
- Added cost table and explanation of why 2-5k samples are needed (not just top-K)
- Added explanation of why targeted > random resampling
- File updated: wiki/analyses/isp-register-optimization.md

---

## [2026-05-09] update | Pipeline correction across all analyses

- Corrected pipeline: simulator = raw + registers → RGB only; IQ measurement is a separate tool
- Raw input is fixed (same test scene with chart targets: MTF, false color, desaturation, etc.)
- 300 runs/min covers both simulator + IQ measurement together
- Removed overclaim: register → metric mapping is still unknown; only register → ISP block is known from C++
- Files updated: Problem_Definition.md, isp-register-optimization.md, cma-es-step-by-step.md, cma-es-explained.md, cpp-register-profiling-workflow.md

---

## [2026-05-09] analysis | CMA-ES Step-by-Step Breakdown

- Analysis page: wiki/analyses/cma-es-step-by-step.md
- One diagram per step: init, sampling, evaluation+ranking, mean update, evolution paths (p_c + p_sigma), CSA step size, covariance update (rank-1 + rank-mu), termination, full loop, what C learns, variants
- index.md updated

---

## [2026-05-09] query | CMA-ES Algorithm and BBO Relationship

- Question: what is CMA-ES and how does it relate to black-box optimization?
- Analysis page: wiki/analyses/cma-es-explained.md
- Covers: core loop, m/C/σ updates, rank-invariance, inverse Hessian insight, CMA-ES vs BO regime, ISP application, variants table
- index.md updated

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
