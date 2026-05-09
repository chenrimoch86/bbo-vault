# Wiki Index

Content catalog. Updated on every ingest or analysis. Read this first when answering queries.

---

## Sources

- [[llm-wiki-idea]] — Core pattern: LLM-maintained persistent wiki vs. RAG (2026-05-08)
- [[bartz-beielstein-2016-surrogate-bbo]] — Survey: surrogate models, DOE, infill criteria for BBO (2026-05-08)
- [[wang-2018-ebo]] — EBO: additive GP ensemble + Mondrian forests; scales BO to 10K+ observations (2026-05-08)
- [[gonzalez-2024-hdbo-survey]] — NeurIPS 2024 HDBO survey; 7-category taxonomy + `poli` benchmark (2026-05-08)
- [[eriksson-2019-turbo]] — TuRBO: trust-region BO with multi-armed bandit; NeurIPS 2019 (2026-05-08)
- [[adascale-turbo-2026]] — AdaScale-TuRBO: GP degeneracy diagnosis + scaled lengthscale prior (2026-05-08)
- [[mg-turbo-2026]] — MG-TuRBO: memory-guided restarts via basin clustering; 84D traffic calibration (2026-05-08)
- [[namura-2024-rei]] — REI: regional EI acquisition function with TR optimality guarantee; Fujitsu (2026-05-08)
- [[anahideh-2019-hdbbo-uncertainty]] — TK-MARS + Smart-Replication for high-D noisy BBO (2026-05-08)
- [[koratikere-2025-snbo]] — SNBO: NN surrogate without uncertainty estimation; 10D–102D (2026-05-08)
- [[hansen-cma-es-reference]] — CMA-ES reference implementation and tutorial by Nikolaus Hansen (2026-05-08)
- [[loshchilov-2017-lm-ma-es]] — LM-MA-ES: O(n log n) evolution strategy for large-scale BBO (2026-05-08)
- [[nomura-2024-lra-cma-es]] — LRA-CMA-ES: online learning rate adaptation via SNR tracking (2026-05-08)
- [[yang-2023-opro]] — OPRO: LLMs as optimizers via meta-prompting; Google DeepMind (2026-05-08)
- [[liu-2024-llambo]] — LLAMBO: LLM as surrogate + warmstarting for BO; ICLR 2024 (2026-05-08)
- [[chang-2025-llinbo]] — LLINBO: federated-learning-inspired LLM weighting in BO loop (2026-05-08)
- [[meindl-2025-gptopt]] — GPTOpt: Llama 3.1 fine-tuned on 2M BO trajectories as GP surrogate (2026-05-08)
- [[li-2025-llamea-bo]] — LLaMEA-BO: LLM evolves complete Python BO algorithm classes (2026-05-08)
- [[huo-2025-bora]] — BORA: adaptive LLM/BO switching based on GP uncertainty; IJCAI 2025 (2026-05-08)
- [[naphade-2025-tcs-hpt]] — TCS: expert block enables small LLMs to match GPT-4 on HPT (2026-05-08)
- [[wang-2025-llm-hpo-uav]] — LLM agent via MCP for UAV algorithm HPO; domain-specific (2026-05-08)
- [[ashouri-2018-compiler-autotuning-survey]] — ACM survey: 200+ papers on ML for compiler optimization (2026-05-08)
- [[trofin-2021-mlgo]] — MLGO: first production ML-guided LLVM pass (inlining-for-size); Google (2026-05-08)
- [[mlgo-google-blog-2022]] — MLGO deployment: 6.3% Fuchsia code reduction + regalloc-for-perf (2026-05-08)
- [[venkatakeerthy-2022-rl4real]] — RL4ReAl: multi-agent RL for LLVM register allocation; CC 2023 (2026-05-08)
- [[grace-2025]] — GRACE: pass synergy + contrastive learning + GA; 10% over -Oz (2026-05-08)
- [[jin-2025-verilocc]] — VeriLocc: LLM + Z3 SMT for GPU regalloc; beats rocBLAS 11.6% (2026-05-08)
- [[burns-2000-slanted-edge-mtf]] — Slanted-edge MTF: ISO 12233 SFR algorithm, bias sources, what the MTF score measures (2026-05-10)
- [[chen-2016-xgboost]] — XGBoost: gradient boosted trees, three importance types (gain/cover/freq), sparsity-aware (2026-05-10)
- [[sacks-1989-dace]] — DACE: foundational GP surrogate + space-filling design for expensive computer experiments (2026-05-10)
- [[mckay-1979-lhs]] — LHS: space-filling sampling; lower variance than random for 200D register space (2026-05-10)
- [[lundberg-2017-shap]] — SHAP: game-theoretic feature importance; consistent, handles correlated registers (2026-05-10)
- [[lundberg-2018-treeshap]] — TreeSHAP: exact O(TLD²) SHAP for XGBoost/LightGBM; practical register importance tool (2026-05-10)
- [[herman-2017-salib]] — SALib: Morris screening + Sobol indices in Python; dead-register identification (2026-05-10)
- [[iooss-2010-q2-metamodel-validation]] — Q2 coefficient: LOO cross-validation metric for surrogate quality; threshold Q2>0.95 for optimization (2026-05-10)
- [[deb-2002-nsga-ii]] — NSGA-II: fast elitist multi-objective GA; returns full MTF/false-color/desaturation Pareto front (2026-05-10)
- [[daulton-2020-qehvi]] — qEHVI: differentiable expected hypervolume improvement for parallel multi-objective BO (2026-05-10)
- [[constantine-2014-active-subspaces]] — Active subspaces: gradient-based dimension reduction; 200D → low-D via rotated coordinates (2026-05-10)
- [[settles-2009-active-learning]] — Active learning survey: QBC framework; theoretical backing for ISP targeted resampling loop (2026-05-10)
- [[wei-2022-chain-of-thought]] — Chain-of-Thought: few-shot prompting with reasoning steps; foundational for ISP C++ extraction (2026-05-10)
- [[roziere-2023-code-llama]] — Code Llama: Meta's code-specialized LLM; 34B Instruct recommended for ISP block analysis (2026-05-10)
- [[hou-2023-llms-for-se]] — LLMs for SE survey: 395 papers; maps reliable vs. unreliable LLM code tasks (2026-05-10)

---

## Entities

- [[vannevar-bush]] — Author of "As We May Think" (1945); described the Memex (2026-05-08)
- [[nikolaus-hansen]] — Creator of CMA-ES; INRIA (2026-05-08)
- [[david-eriksson]] — Creator of TuRBO; Cornell / Uber AI (2026-05-08)
- [[google]] — Google / Google Research / Google DeepMind; MLGO, OPRO, EBO (2026-05-08)
- [[llvm]] — Open-source compiler infrastructure; dominant platform for autotuning research (2026-05-08)

---

## Concepts

- [[rag]] — Standard retrieval pattern; re-derives answers from raw docs on every query (2026-05-08)
- [[compounding-knowledge]] — Wiki property: each new source enriches existing pages, not just adds content (2026-05-08)
- [[memex]] — Bush's 1945 concept for associative personal knowledge storage (2026-05-08)
- [[schema-file]] — The CLAUDE.md/AGENTS.md doc that turns an LLM into a disciplined wiki agent (2026-05-08)
- [[bayesian-optimization]] — Sequential model-based optimization: GP surrogate + acquisition function (2026-05-08)
- [[gaussian-process]] — Probabilistic surrogate; O(n³); posterior mean + variance for acquisition (2026-05-08)
- [[acquisition-function]] — Balances exploration/exploitation: EI, UCB, PI, Thompson sampling, REI (2026-05-08)
- [[trust-region-bo]] — Local BO in adaptive hyperrectangle; TuRBO, AdaScale, MG-TuRBO, REI (2026-05-08)
- [[cma-es]] — Second-order evolution strategy; CMA-ES, MA-ES, LM-MA-ES, LRA-CMA-ES (2026-05-08)
- [[high-dimensional-bo]] — Strategies for D>20 BO: trust regions, additive models, embeddings, NN (2026-05-08)
- [[surrogate-model]] — Polynomial, RBF, GP/kriging, NN, MARS as cheap function approximators (2026-05-08)
- [[llm-bo-hybrid]] — LLMs as optimizers, surrogates, or adaptive BO components (2026-05-08)
- [[compiler-autotuning]] — ML/RL for pass selection and phase ordering in LLVM/GCC (2026-05-08)
- [[hyperparameter-optimization]] — HPO as BBO; BO, LLM, and hybrid approaches (2026-05-08)
- [[image-quality-metrics]] — MTF, false color, desaturation: what each measures and which ISP registers drive it (2026-05-10)
- [[sensitivity-analysis]] — Morris/Sobol/TreeSHAP: ranking which registers matter per IQ metric (2026-05-10)
- [[multi-objective-optimization]] — Pareto front, NSGA-II, qEHVI: optimizing MTF/false-color/desaturation jointly (2026-05-10)
- [[latin-hypercube-sampling]] — Space-filling design for 200D; lower variance than random for surrogate fitting (2026-05-10)
- [[active-learning]] — Query-by-committee adaptive sampling; theoretical backing for ISP targeted retraining loop (2026-05-10)
- [[metamodel-validation]] — Q2 coefficient, regional validation, acceptance threshold before trusting surrogate (2026-05-10)

---

## Analyses

- [[mermaid-diagram-demo]] — Demo: 6 Mermaid diagram types (flowchart, taxonomy, state, concept map, timeline, quadrant) using real wiki content (2026-05-08)
- [[llm-bo-integration-patterns]] — Synthesis: 5 patterns for combining LLMs with BO + improvements each delivers (2026-05-08)
- [[isp-register-optimization]] — Recommendation: BBO method selection for ~200 ISP registers → image quality optimization (2026-05-08)
- [[Problem_Definition]] — Full problem definition: ISP register optimization, constraints, current approach, recommended direction (2026-05-08)
- [[cpp-register-profiling-workflow]] — Workflow: LLM analysis of C++ ISP block files to extract register profiles, effective ranges, dead zones, thresholds (2026-05-08)
- [[cma-es-explained]] — CMA-ES algorithm explained: core loop, update mechanisms, BBO relationship, ISP application, variants (2026-05-09)
- [[cma-es-step-by-step]] — CMA-ES full step-by-step breakdown: init, sampling, ranking, mean update, evolution paths, CSA, covariance update — one diagram per step (2026-05-09)
