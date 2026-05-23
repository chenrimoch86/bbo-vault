---
title: CMA-ES vs GA — Computational Cost & Block Structure (ISP Registers)
type: analysis
tags: [cma-es, genetic-algorithm, computational-cost, separability, surrogate, isp, black-box-optimization]
created: 2026-05-23
updated: 2026-05-23
sources: [Whitley-1994-GA-Tutorial.md, Beyer-Schwefel-2002-Evolution-Strategies-Intro.md, Storn-Price-1997-Differential-Evolution.md, Hrstka-2009-EA-Competitive-Comparison.md, Loshchilov-2017-LM-MA-ES.md, CMA-ES-homepage.md]
---

A focused companion to [[isp-register-optimization]]. That page argues *why* CMA-ES beats GA on continuous landscapes (correlation learning, evolution paths, step-size adaptation). This page covers two angles it underweights: the **computational-cost accounting** and how the **ISP block structure** (partial separability) changes the right answer.

## When to use each (one-line summary)

- **[[genetic-algorithm]]** — discrete / combinatorial / mixed-integer; rugged spaces where crossover recombines meaningful building blocks; with [[multimodal-optimization|niching]] when you want *many* distinct good configs.
- **[[cma-es]]** — continuous, real-valued, ill-conditioned, **non-separable** landscapes; quasi-parameter-free; the default for continuous black-box in ~10–200D (the [[evolution-strategies]] family).
- **[[differential-evolution]]** — a GA-family method that *does* compete on continuous spaces with 3 knobs, but [[hrstka-2009-ea-comparison]] shows it degrades past ~30–50D. A reasonable baseline, not the primary choice at 200D.

## Why CMA-ES matches this landscape — property by property

The deepest argument isn't "CMA-ES is better"; it's that GA's *assumptions* mismatch the actual geometry of this objective. First, the shape of the landscape over the active registers:

1. **Continuous & real-valued** — gains, offsets, thresholds, filter coefficients.
2. **Correlated / tilted** — ISP blocks couple registers (sharpening ↔ noise-reduction trade-off; gains scaling together). The high-IQ region is a thin, tilted ridge, not an axis-aligned box.
3. **Anisotropic / ill-conditioned** — registers differ in scale (8- vs 16-bit fields) and sensitivity; curvature differs by orders of magnitude across directions.
4. **Block-structured** — ~15–16 groups of ~a dozen; the true Hessian is ≈ block-diagonal.
5. **Smooth-ish** — over the XGBoost ensemble, an approximately continuous, locally-quadratic surface.
6. **Mildly multimodal** — different register regimes give locally-good IQ.

### What counts as "continuous" — smoothness, not monotonicity, and not storage width

This is the property most often misjudged, so be precise. A register is **continuous (for optimization)** when its values are **ordered** and the response is **locally smooth** — *nudging it a little changes the image a little*. Three corrections to the naive view:

- **Continuous ≠ monotonic.** A register need not push IQ in one direction. A noise-reduction or coring **threshold** typically has a *sweet spot*: too low lets noise through, too high over-smooths, best in the middle — the slope *reverses* at the optimum. That is still continuous; it's a hill with a peak, which is exactly what an optimizer hunts. Direction flipping mid-range is the normal case, not a problem.
- **Storage width ≠ type.** "8/16/24-bit" is *resolution* (256 / 65,536 / 16.7M ordered levels), not category. A 16-bit gain is a finely-quantized **dial**, i.e. quasi-continuous — *not* discrete. The tilted-ridge / anisotropic / block geometry above applies to it unchanged.
- **Truly discrete = label, not quantity.** A register is categorical only when **+1 jumps to an unrelated behavior**: a mode select, enable bit, mux select, enum index, packed bitfield. That holds regardless of bit width.

Threshold-style registers stay firmly on the CMA-ES side, and their quirks favor CMA-ES over GA rather than the reverse:
- **Plateaus** (a threshold that doesn't trigger over part of the range → flat score): CMA-ES's σ *grows* to stride across the flat zone until it finds slope again; GA has no analogue.
- **Kinks** (a sharp bend where the threshold starts clamping): CMA-ES is derivative-free and rank-based, so non-differentiable bends don't break it.
- **Multiple peaks**: handled by multi-start / IPOP restart ([[auger-hansen-2005-ipop-cma-es]]).

The only thing that would actually defeat CMA-ES is a *non-smooth, orderless* response (pure noise / categorical) — which threshold registers are not.

**Integer handling.** CMA-ES samples continuous values and **rounds to the integer grid**. The one failure mode: when σ shrinks below ~1 LSB, all samples round to the same integer and that coordinate stalls. For 8/16/24-bit registers this essentially never happens (the grid is far finer than the precision IQ needs), so plain rounding works. It only bites for *low-cardinality* integers (binary / few-level), where the fix is **CMA-ES with Margin** (Hamano/Nomura et al., GECCO 2022 — adjacent to [[nomura-2024-lra-cma-es]], not yet ingested) or `pycma`'s `integer_variables` option.

**Quick per-register test:** *"If I increase this register by one step, does the image change a little (smoothly), or jump to something unrelated?"* Smooth → continuous → CMA-ES. Jump/mode/flag → categorical → handle separately (below). The C++ source disambiguates: `pixel * gain >> shift` is ordinal; `if (mode == 2)` is categorical — see [[cpp-register-profiling-workflow]].

### Property 1+2: correlated, tilted optimum — the decisive factor

Two registers that must rise *together*:
```
Parent A: R12=200, R45=10    Parent B: R12=50, R45=180
```
**GA crossover is a coordinate-axis operation** — it swaps register *values*, so recombining A and B yields the useful `(200,180)` or the worst `(50,10)` on a coin flip. It cannot represent "move R12 and R45 together"; for every correlation it builds it destroys one. The schema theorem's building-block argument assumes the coordinate decomposition aligns with the problem's structure — there is no reason register *indexing* aligns with ISP register *interactions*. **GA mutation is axis-aligned**: on a 45° ridge, steps are mostly perpendicular → rejected → wasted.

**CMA-ES samples from `N(m, σ²C)` where `C` is a learned rotation+scaling.** The off-diagonal `C[12,45]` grows once high-R12+high-R45 candidates rank well, so the sampling ellipse **rotates to lie along the ridge** and steps move along it by construction.

### Property 3: anisotropic scaling

GA uses one fixed step distribution per coordinate — no way to know R30 needs tiny nudges while R7 wants large ones. CMA-ES's `C` approximates the **inverse Hessian**: large steps in flat directions, small in steep ones. This is why CMA-ES is the standard for ill-conditioned continuous problems.

### The deep reason — invariances match the *unknown* structure

CMA-ES has two invariances that are exactly right when the structure is unknown (register→metric mapping *is* unknown here):

- **Invariant to monotonic transforms of the objective** — CMA-ES uses only candidate *rankings*. Reweighting/rescaling the IQ-metric blend (MTF vs false-color vs desaturation), or adding nonlinear penalties, does not change its trajectory. Fitness-proportionate GA selection is sensitive to fitness scale (one metric can dominate; needs hand-tuned scaling).
- **Invariant to affine transforms of the search space** (rotation+scaling, once `C` adapts) — performance doesn't depend on how a block was parameterized. GA's coordinate-wise crossover and axis-aligned mutation are *not* rotation-invariant; their behavior depends on the arbitrary register axis-parameterization.

Because the register coupling and metric weighting are arbitrary and unknown, you want an optimizer whose behavior doesn't depend on those choices — the [[evolution-strategies]] self-adaptation philosophy ([[beyer-schwefel-2002-evolution-strategies]]).

### Property 4: block structure

`C` naturally drives cross-block off-diagonals toward zero, or you impose a block-diagonal `C` (see the dedicated section below). GA has no representation-level analogue — crossover treats all 200 coordinates identically.

### Property 5+6: step-size control and getting unstuck

CMA-ES's **CSA** grows σ on consistent progress and shrinks it near the optimum → precise final convergence (small register changes shift IQ). GA mutation noise floors achievable precision. For the mild multimodality, **IPOP/multi-start CMA-ES** ([[auger-hansen-2005-ipop-cma-es]]) is a principled escape; GA niching ([[multimodal-optimization]]) solves the *different* problem of keeping many optima, which you don't need (you want one best config).

### The honest counterpoint — where GA-style logic belongs

Pure CMA-ES assumes continuous variables. If a subset of registers are genuinely **discrete/categorical** — i.e. *labels, not quantities* (mode selects, enable bits, demosaic-algorithm choice, mux selectors) — don't switch to GA wholesale; **split by type**: continuous/quantized registers → CMA-ES (with rounding); categorical registers → mixed-integer CMA-ES-with-margin, or an outer GA/enumeration loop with CMA-ES optimizing the continuous registers inside each branch. Note that *ordinal* integers (tap counts, gains, thresholds) are **not** in this discrete bucket — they are quasi-continuous dials and stay on CMA-ES (see the continuity discussion above). [[cpp-register-profiling-workflow]] is how you classify each register.

**Net:** GA is mismatched on five of six landscape properties (blind to correlations, axis-locked, scale-sensitive, can't exploit blocks, no principled step control); CMA-ES matches all five, and its invariances are precisely the robustness you want under unknown coupling and arbitrary metric weighting. GA-style logic earns its place only on the genuinely discrete register subset.

## Mixed continuous + categorical registers

In practice the register set is **mixed**: continuous/ordinal dials *and* categorical registers (enable/disable bits, mode selects). This is mixed-integer / mixed-variable black-box optimization — the one regime where *plain* CMA-ES is genuinely weak — so it needs an explicit architecture.

### Three register types, by difficulty

| Type | Example | For CMA-ES |
|---|---|---|
| Continuous / ordinal | gain, threshold, coefficient (8/16/24-bit) | Native |
| Binary | enable/disable, on/off flag | Easy — 2 values, no fake-ordering issue |
| Categorical, k≥3, unordered | demosaic mode {bilinear, AHD, gradient} | Hard — needs special handling |

The difficulty axis is **order**. CMA-ES follows "which direction is better"; an unordered k-way mode has no number line to follow (no reason mode 1 is "between" 0 and 2).

### Why not flatten everything into one vector

1. **Unordered modes get a fake order.** Rounding a mode to {0,1,2} pretends mode 1 sits between 0 and 2; CMA-ES then tries to "interpolate" toward a mode, which is meaningless.
2. **Categoricals change which continuous registers even matter.** Disabling a block makes its gain/threshold registers **inert**; switching mode activates a *different* coefficient set. The continuous landscape is **conditional** on the categorical settings — a flat 200-vector wastes budget tuning dead dimensions.

### Recommended architecture — outer categorical → inner CMA-ES

```
for each combination of {modes, enable bits}:        ← outer loop
    mask out registers that are inert in this branch
    run CMA-ES on the remaining continuous registers  ← inner loop (its home turf)
keep the best (branch, continuous-config) overall
```

- **Masking** is the key win: inert registers are dropped from the CMA-ES vector per branch, so it only searches dimensions that affect IQ. [[cpp-register-profiling-workflow]] reveals which registers go inert under which settings.
- Over the **frozen XGBoost surrogate** (microsecond queries) running many inner CMA-ES instances is effectively free, so this is cheap here specifically.

**Decision rule — count the categorical combinations:**
- **Small** (≤ a few hundred): **enumerate** the outer loop, inner CMA-ES each. Exhaustive over modes, robust.
- **Large**: coordinate the categoricals with a GA / random / TPE search, CMA-ES still doing the continuous inner loop. This is the *one* place GA-style search legitimately belongs in this problem — searching unordered categorical combinations.

### In-loop alternative (no outer loop)

**CMA-ES with Margin** (Hamano/Nomura, GECCO 2022; adjacent to [[nomura-2024-lra-cma-es]], not yet ingested) — the principled mixed-integer CMA-ES. It keeps a *margin* (floor on each discrete level's marginal probability) so the distribution can't collapse below the grid; handles binary and ordinal integers well, and unordered modes via one-hot encoding (one continuous score per mode, take argmax). `pycma`'s `integer_variables` option covers the ordinal/binary part. Simpler to wire up, but does not exploit the conditional/inert structure as cleanly as the outer/inner split.

### Practical steps

1. **Classify** each register: continuous/ordinal vs binary vs k-way mode (C++ source + SHAP).
2. **Binary enables** → keep in the CMA-ES vector with margin/thresholding, or fold into the outer loop when they gate whole blocks (enables masking).
3. **Unordered modes** → outer loop (enumerate if few, GA/random if many).
4. **Continuous core** → CMA-ES, **inert registers masked per branch**.
5. Validate the best `(mode, config)` on the simulator.

CMA-ES still does the heavy lifting on the continuous core; the wrapper picks the branch and masks dead registers rather than pretending modes live on a number line.

## Two cost axes (don't conflate them)

### (a) Internal per-iteration overhead of the algorithm

| | Cost | At n=200 | After reduction to 20–40 |
|---|---|---|---|
| GA | `O(pop × D)` per generation | negligible | negligible |
| CMA-ES | `O(n²)` covariance + periodic `O(n³)` eigendecomposition | ~ms, the one real overhead | trivial |

If staying **native 200D** and overhead matters, use **[[loshchilov-2017-lm-ma-es]]** (LM-MA-ES): `O(n log n)` time/space, same quality.

### (b) Number of objective evaluations to converge (sample efficiency)

CMA-ES converges in far fewer evaluations on continuous landscapes because it learns geometry; GA wastes evaluations on correlation-destroying crossover and axis-aligned mutation.

## The surrogate changes the calculus

The objective here is a **frozen XGBoost surrogate** — each query is microseconds, so evaluations are effectively free (millions are fine). Consequences:

1. **Axis (b) stops mattering for raw compute.** GA's wastefulness in query count is affordable.
2. **It still matters for solution quality.** With unlimited XGBoost queries, GA still gets stuck in local optima and can't follow diagonal/correlated directions → returns a *worse* config. CMA-ES finds a *better* one. **Switching to CMA-ES buys quality, not compute savings.**
3. **Axis (a) is the only added cost**, and against microsecond queries it is negligible at 20–40D.
4. **The expensive oracle is untouched during search.** The C++ ISP simulator + IQ tool (~300/min) feeds *training data and validation only* — neither GA nor CMA-ES calls it in the loop. So optimizer choice does not move the expensive-evaluation budget at all.

## Block structure → exploit partial separability

The ~200 registers come in **groups of ~a dozen, each tied to a different digital block** (≈15–16 blocks). This is partial separability and is exploitable:

- **If cross-block interactions are weak**, the problem nearly decomposes. Restrict CMA-ES covariance to **block-diagonal** (model only within-block correlations) — collapses the `O(n²)` cost and speeds convergence — or optimize blocks semi-independently.
- **Interactions are unknown** (per [[Problem_Definition]]) but *measurable for free* from the existing model: **TreeSHAP interaction values** ([[lundberg-2018-treeshap]]) and XGBoost gain importance reveal which registers and cross-block pairs actually interact. Weak → block-diagonal is a safe win; strong → keep full covariance on the active set.
- Dovetails with the standing recommendation: reduce to **~20–40 active registers** via importance + C++ static analysis ([[constantine-2014-active-subspaces]]), *then* multi-start CMA-ES, *then* validate top-K on the simulator and retrain where XGBoost is wrong ([[koratikere-2025-snbo]], [[bartz-beielstein-2016-surrogate-bbo]]).

## Bottom line

Replace GA with **multi-start CMA-ES** over the same frozen XGBoost. It costs essentially the same compute — the covariance overhead is negligible after dimensionality reduction — but returns materially better configs because it learns the register correlations GA destroys. Use **block-diagonal covariance** once SHAP shows cross-block interactions are weak, **LM-MA-ES** if you stay native 200D, and add the **simulator-validation/retraining loop** regardless.

## See also

- [[isp-register-optimization]]
- [[cma-es]]
- [[genetic-algorithm]]
- [[differential-evolution]]
- [[loshchilov-2017-lm-ma-es]]
- [[lundberg-2018-treeshap]]
- [[constantine-2014-active-subspaces]]
