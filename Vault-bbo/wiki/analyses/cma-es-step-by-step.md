---
title: CMA-ES — Step-by-Step Breakdown
type: analysis
tags: [cma-es, evolution-strategy, black-box-optimization, algorithm, tutorial]
created: 2026-05-09
updated: 2026-05-09
sources: [CMA-ES-homepage.md, Loshchilov-2017-LM-MA-ES.md, Nomura-2024-CMA-ES-Learning-Rate.md]
---

Detailed breakdown of every step inside the CMA-ES algorithm, one diagram per step.
See [[cma-es-explained]] for the high-level view and relationship to BBO.

---

## The Problem We Are Solving

### Context

```mermaid
flowchart LR
    A["Fixed raw test scene<br/>always same input"] --> B["Register config<br/>~200 registers"]
    B --> C["C++ ISP Simulator<br/>raw + registers → RGB"]
    C --> D["IQ Measurement tool<br/>analyzes chart regions"]
    D --> E["IQ scores:<br/>MTF, false color<br/>desaturation, ..."]
```

Two distinct steps per evaluation:
- **Simulator** — runs the ISP chain, outputs RGB of the test scene
- **IQ Measurement tool** — analyzes chart regions in the RGB, outputs one score per metric

Together they run at **300 configs/minute** via parallel CPUs. No real hardware involved.

### What Data We Have

```mermaid
flowchart TD
    A["300,000 evaluations<br/>register config → IQ scores"] --> B["XGBoost surrogate<br/>trained on 300k pairs"]
    B --> C["Predicts IQ metrics<br/>from registers directly"]
    C --> D["Feature importance<br/>per register per metric"]
    D --> E["Active subspace:<br/>~20-40 registers of 200"]
```

| Asset | Details |
|---|---|
| Training data | 300k (register config, IQ scores) pairs — ~16h of compute |
| Surrogate | XGBoost: registers → predicted IQ scores |
| C++ source | One file per ISP block — gives register → ISP block mapping only |
| Full evaluation | Simulator + IQ measurement, 300/min parallelized |
| Unknown | Which registers affect which metrics — found via XGBoost feature importance |

### The Goal

```mermaid
flowchart LR
    A["Find register config x*"] --> B["Maximizes weighted IQ scores<br/>f(x*) = max over all x"]
    B --> C["Validated by full evaluation<br/>simulator + IQ measurement"]
    C --> D["XGBoost prediction<br/>matches true IQ score"]
```

### Why CMA-ES and Not GA

```mermaid
flowchart TD
    A["Current approach:<br/>GA with random starts<br/>over frozen XGBoost"] --> B["Problems:<br/>GA designed for discrete problems<br/>poor in continuous 200D<br/>no surrogate validation loop"]
    B --> C["CMA-ES replacement:<br/>designed for continuous high-D<br/>adapts to register correlations<br/>paired with iterative retraining"]
```

CMA-ES queries XGBoost millions of times for free (microsecond inference). After finding a promising region, the top configs are validated on the simulator and XGBoost is retrained on targeted samples if it disagrees. See [[isp-register-optimization]] for the full pipeline.

---

## The Three Things CMA-ES Maintains

Before the steps: CMA-ES tracks three quantities that fully define the search distribution at any point in time.

```mermaid
flowchart LR
    A["m<br/>Mean vector<br/>WHERE to search"] 
    B["sigma<br/>Step size<br/>HOW FAR to search"]
    C["C<br/>Covariance matrix<br/>WHAT SHAPE to search"]
    D["Search distribution<br/>N(m, sigma^2 * C)"]
    A --> D
    B --> D
    C --> D
```

All three are adapted every generation based on the ranking of sampled candidates.

---

## Step 0 — Initialization

Set up all parameters before the first generation.

```mermaid
flowchart TD
    A([Start]) --> B["Set starting point m<br/>initial guess or random"]
    B --> C["Set step size sigma<br/>typically range / 3"]
    C --> D["Set covariance C = I<br/>identity: isotropic, no preference"]
    D --> E["Set evolution paths p_c = 0, p_sigma = 0<br/>empty history"]
    E --> F["Compute population size<br/>lambda = 4 + floor(3 * ln(n))"]
    F --> G["Compute parents count<br/>mu = lambda / 2"]
    G --> H["Compute recombination weights<br/>w_i decreasing, sum to 1"]
    H --> I([Ready to sample])
```

**Key defaults for your ISP problem (n = 40 active registers):**

| Parameter | Formula | Value (n=40) |
|---|---|---|
| λ (population) | 4 + floor(3·ln(n)) | ~15 candidates/generation |
| μ (parents) | λ / 2 | ~7 selected |
| σ (step size) | register range / 3 | set per register |
| C | Identity matrix | isotropic start |

---

## Step 1 — Sampling

Draw λ candidate solutions from the current search distribution.

```mermaid
flowchart TD
    A["Current distribution<br/>N(m, sigma^2 * C)"] --> B["Eigendecompose C<br/>C = B * D^2 * B^T<br/>B = eigenvectors, D = sqrt eigenvalues"]
    B --> C["For each of lambda candidates:<br/>draw z_i from N(0, I)"]
    C --> D["Transform: x_i = m + sigma * B * D * z_i"]
    D --> E["Result: lambda candidates<br/>x_1, x_2, ..., x_lambda<br/>sampled around m"]
```

**Intuition:** B rotates the sample to align with C's eigenvectors. D scales each axis by the corresponding eigenvalue. This means the cloud of candidates has the same shape as C — ellipsoidal, aligned with the landscape.

```mermaid
flowchart LR
    subgraph Round1 ["Early: C = I (sphere)"]
        A1(["o"]) 
        A2(["o"])
        A3(["o"])
        A4(["m"])
        A5(["o"])
        A6(["o"])
    end
    subgraph Round2 ["Later: C adapted (ellipse)"]
        B1(["o"])
        B2(["o"])
        B3(["m"])
        B4(["o"])
        B5(["o"])
    end
    Round1 -- "C adapts to landscape" --> Round2
```

---

## Step 2 — Evaluation and Ranking

Evaluate the true (black-box) function on each candidate and rank them.

```mermaid
flowchart TD
    A["lambda candidates<br/>x_1, ..., x_lambda"] --> B["Evaluate f(x_i)<br/>for each candidate<br/>black-box call"]
    B --> C["Rank by f value<br/>best = rank 1"]
    C --> D["Select top mu candidates<br/>x_1:lambda, x_2:lambda, ..., x_mu:lambda"]
    D --> E["Assign weights w_i<br/>rank 1 gets highest weight<br/>rank mu gets lowest weight"]
```

**Only ranks matter — not magnitudes.** Whether the best candidate scores 0.1 or 1000 is irrelevant. Only that it ranked first. This makes CMA-ES invariant to any monotonic transformation of f — including your XGBoost predictions, which only need to rank correctly, not be calibrated.

---

## Step 3 — Mean Update (Recombination)

Move the search center toward the weighted centroid of the top-μ candidates.

```mermaid
flowchart TD
    A["Top mu candidates<br/>x_1:lambda, ..., x_mu:lambda"] --> B["Weighted centroid:<br/>m_new = sum(w_i * x_i:lambda)<br/>for i = 1 to mu"]
    B --> C["Step taken:<br/>delta_m = m_new - m_old"]
    C --> D["Update mean:<br/>m = m_new"]
```

**Intuition:** the mean shifts toward the best candidates. The weight w_1 > w_2 > ... > w_μ means the best candidate pulls harder than the second-best, and so on. This is a weighted gradient step without computing any gradient.

```mermaid
flowchart LR
    A(["x_3 w=0.1"]) --> D
    B(["x_2 w=0.3"]) --> D
    C(["x_1 w=0.6"]) --> D
    D(["m_new<br/>weighted centroid"])
    E(["m_old"]) -- "shifts toward" --> D
```

---

## Step 4 — Evolution Path Update

Two evolution paths are maintained: **p_c** (for covariance update) and **p_sigma** (for step size control). Both accumulate the history of mean shifts.

### 4a — Step Size Evolution Path (p_sigma)

```mermaid
flowchart TD
    A["Previous p_sigma"] --> B["Decay old path:<br/>(1 - c_sigma) * p_sigma"]
    C["Mean shift this generation:<br/>(m_new - m_old) / sigma"] --> D["Decorrelate:<br/>multiply by B^T<br/>removes C's influence"]
    D --> E["Scale by sqrt(c_sigma*(2-c_sigma)*mu_eff)"]
    B --> F["p_sigma_new = decay + scaled shift"]
    E --> F
```

p_sigma lives in the isotropic space (after removing C's rotation). It measures how consistently the mean is moving — if it moves in the same direction repeatedly, p_sigma grows long.

### 4b — Covariance Evolution Path (p_c)

```mermaid
flowchart TD
    A["Previous p_c"] --> B["Decay old path:<br/>(1 - c_c) * p_c"]
    C["Mean shift this generation:<br/>(m_new - m_old) / sigma"] --> D["Scale by sqrt(c_c*(2-c_c)*mu_eff)"]
    B --> E["p_c_new = decay + scaled shift"]
    D --> E
```

p_c accumulates the raw mean shifts (not decorrelated). It captures the direction in which the search is progressing — used to update C.

---

## Step 5 — Step Size Adaptation (CSA)

Adjust σ based on the length of p_sigma compared to what a random walk would produce.

```mermaid
flowchart TD
    A["Compute ||p_sigma||<br/>length of step size evolution path"] --> B{"Compare to expected<br/>random walk length<br/>E||N(0,I)|| ~= sqrt(n)"}
    B -- "||p_sigma|| > expected<br/>moving consistently" --> C["Increase sigma<br/>sigma * exp(positive)"]
    B -- "||p_sigma|| == expected<br/>random walk behavior" --> D["Keep sigma unchanged"]
    B -- "||p_sigma|| < expected<br/>oscillating or stuck" --> E["Decrease sigma<br/>sigma * exp(negative)"]
    C --> F["sigma_new = sigma * exp(c_sigma/d_sigma * (||p_sigma||/E||N(0,I)|| - 1))"]
    D --> F
    E --> F
```

**Intuition — why this works:**
- If the mean moves in the same direction many generations in a row, p_sigma accumulates and grows long → increase σ to take bigger steps
- If the mean oscillates back and forth, p_sigma stays short → decrease σ to avoid overshooting
- Targets the random walk length as the "neutral" reference

```mermaid
flowchart LR
    subgraph Consistent ["Consistent progress"]
        direction TB
        G1["gen1: move right"] --> G2["gen2: move right"] --> G3["gen3: move right"]
        G3 --> G4["p_sigma long → sigma UP"]
    end
    subgraph Oscillating ["Oscillating"]
        direction TB
        H1["gen1: move right"] --> H2["gen2: move left"] --> H3["gen3: move right"]
        H3 --> H4["p_sigma short → sigma DOWN"]
    end
```

---

## Step 6 — Covariance Matrix Update

Update C to reflect the shape of the high-performing region. Two complementary updates are combined.

### 6a — Rank-1 Update (from evolution path)

```mermaid
flowchart TD
    A["p_c: accumulated direction<br/>of successful mean shifts"] --> B["Outer product:<br/>p_c * p_c^T<br/>rank-1 matrix"]
    B --> C["Scale by c_1 (small learning rate)"]
    C --> D["C_rank1 = c_1 * p_c * p_c^T<br/>elongates C toward p_c direction"]
```

The rank-1 update uses the long-term direction of search progress. If the mean has been consistently moving toward (register_A high, register_B low), p_c points that way and C gets elongated in that direction.

### 6b — Rank-mu Update (from current generation)

```mermaid
flowchart TD
    A["Top mu candidates<br/>x_1:lambda, ..., x_mu:lambda"] --> B["Compute step directions:<br/>y_i = (x_i:lambda - m_old) / sigma"]
    B --> C["Weighted outer products:<br/>sum(w_i * y_i * y_i^T)<br/>for i = 1 to mu"]
    C --> D["Scale by c_mu"]
    D --> E["C_rankmu = c_mu * sum(w_i * y_i * y_i^T)<br/>reflects shape of top candidates THIS generation"]
```

The rank-μ update learns from where the best candidates were in the current generation — a fast, short-term signal.

### 6c — Full Covariance Update

```mermaid
flowchart TD
    A["Old C"] --> B["Decay: (1 - c_1 - c_mu) * C"]
    C["Rank-1 term:<br/>c_1 * p_c * p_c^T"] --> D
    E["Rank-mu term:<br/>c_mu * sum(w_i * y_i * y_i^T)"] --> D
    B --> D["C_new = decay + rank1 + rankmu"]
```

**Why both updates?**
- Rank-1 uses cumulated history → good for long-range correlation, slow to adapt
- Rank-μ uses current generation → fast response, but noisier
- Together they balance stability and responsiveness

---

## Step 7 — Termination Check

```mermaid
flowchart TD
    A["After each generation"] --> B{"Termination<br/>condition?"}
    B -- "Max evaluations reached" --> C([Stop: budget exhausted])
    B -- "sigma too small<br/>sigma < sigma_min" --> D([Stop: converged])
    B -- "No improvement<br/>over many generations" --> E([Stop: stagnation])
    B -- "Condition number of C<br/>too large" --> F([Stop: ill-conditioned])
    B -- "None triggered" --> G["Increment generation<br/>go to Step 1 Sampling"]
```

For your ISP problem: set max evaluations based on your XGBoost query budget (millions are free), not simulator budget.

---

## Complete CMA-ES Loop

```mermaid
flowchart TD
    A([Initialize<br/>m, sigma, C, paths]) --> B
    B["Sample lambda candidates<br/>from N(m, sigma^2 * C)"] --> C
    C["Evaluate f on each candidate<br/>XGBoost inference: free"] --> D
    D["Rank and select<br/>top mu candidates"] --> E
    E["Update mean m<br/>toward top-mu centroid"] --> F
    F["Update evolution paths<br/>p_sigma and p_c"] --> G
    G["Adapt step size sigma<br/>via CSA"] --> H
    H["Update covariance C<br/>rank-1 + rank-mu"] --> I
    I{"Termination?"} -- No --> B
    I -- Yes --> J(["Return best x seen"])
```

---

## What C Learns Over Time

The covariance matrix C is the most powerful part of CMA-ES. It learns the geometry of the objective function's level sets.

```mermaid
flowchart TD
    subgraph Gen1 ["Generation 1-10: C = I (sphere)"]
        A1["Candidates spread<br/>equally in all directions"]
    end
    subgraph Gen2 ["Generation 10-50: C adapting"]
        A2["Candidates elongating<br/>toward promising directions"]
    end
    subgraph Gen3 ["Generation 50+: C converged"]
        A3["Candidates aligned with<br/>objective level sets<br/>efficient search ellipse"]
    end
    Gen1 --> Gen2 --> Gen3
```

**For ISP registers:** if registers R12 and R45 must increase together to improve sharpness (correlated), C learns this correlation and samples candidates that move both registers simultaneously. GA would have to stumble onto this by chance. CMA-ES discovers it systematically.

---

## Why It Works for Black-Box Problems

```mermaid
flowchart LR
    A["Black-box function f<br/>no gradient available"] --> B["CMA-ES uses only<br/>rank of f(x_i)"]
    B --> C["Rank-invariant:<br/>f or log(f) or f^2<br/>gives identical result"]
    C --> D["Learns geometry<br/>from ranking patterns<br/>across generations"]
    D --> E["Approximates inverse Hessian<br/>in C without any derivative"]
```

---

## Variants — When to Use Which

```mermaid
flowchart TD
    A{"Problem<br/>dimensionality"} --> B["n < 100<br/>Standard CMA-ES<br/>O(n^2), reference impl"]
    A --> C["n = 100 to 1000<br/>LM-MA-ES<br/>O(n log n)"]
    A --> D["n > 1000<br/>Diagonal CMA-ES<br/>O(n), loses rotation invariance"]
    E{"Landscape<br/>type"} --> F["Noisy or multimodal<br/>LRA-CMA-ES<br/>auto-adapts learning rate"]
    E --> G["Many local optima<br/>BIPOP-CMA-ES<br/>restarts with growing population"]
```

For your ISP problem: **standard CMA-ES** on 20–40D reduced space, or **LM-MA-ES** if running on full 200D.

---

## See also

- [[cma-es]]
- [[cma-es-explained]]
- [[hansen-cma-es-reference]]
- [[loshchilov-2017-lm-ma-es]]
- [[nomura-2024-lra-cma-es]]
- [[isp-register-optimization]]
- [[bayesian-optimization]]
