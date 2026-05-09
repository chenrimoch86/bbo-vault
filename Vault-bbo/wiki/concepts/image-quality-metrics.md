---
title: "Image Quality Metrics"
type: concept
tags: [isp, mtf, false-color, desaturation, image-quality, iq-measurement]
created: 2026-05-10
updated: 2026-05-10
sources: [Burns-2000-Slanted-Edge-MTF.md]
---

The three IQ metrics that define the optimization objective in the ISP register problem. The IQ measurement tool computes all three from the RGB output of the ISP simulator on a fixed test scene (chart with controlled targets).

## MTF — Modulation Transfer Function

**What it measures**: Sharpness / spatial resolution. How accurately the ISP reproduces fine detail at different spatial frequencies.

**How it is computed**: Slanted-edge method (ISO 12233 / Burns 2000 [[burns-2000-slanted-edge-mtf]]). The fixed test scene contains a slanted black-white edge target. The IQ tool computes the SFR (Spatial Frequency Response) by:
1. Extracting the edge region from RGB output
2. Computing the 4× supersampled edge-spread function
3. Taking the DFT → normalized modulus = SFR (reported as MTF)

**Optimization direction**: Maximize (higher = sharper; typical target: MTF50 > threshold).

**ISP registers that affect MTF**: Sharpening/edge enhancement, demosaic filter coefficients, noise reduction (over-smoothing kills MTF).

## False Color

**What it measures**: Color fringing / chromatic aberration artifacts along high-contrast edges. Caused by channel misregistration and demosaic errors.

**Optimization direction**: Minimize (lower = fewer color artifacts).

**ISP registers that affect false color**: Demosaic algorithm parameters, color correction matrix, false color suppression filters.

## Desaturation

**What it measures**: Loss of color saturation — colors appearing washed out or gray. Caused by excessive noise reduction or incorrect color processing.

**Optimization direction**: Minimize (lower = colors are preserved).

**ISP registers that affect desaturation**: Noise reduction aggressiveness, color saturation scaling, gamut mapping.

## Metric Interactions and Trade-offs

The three metrics are not independent:

```
MTF ↑  often requires  NR ↓  which causes  false color ↑
MTF ↑  sometimes causes  desaturation ↑
false color ↓  sometimes requires  chroma filtering ↑  which causes  desaturation ↑
```

This is why the optimization is genuinely multi-objective. The current approach uses a fixed weighted sum; [[deb-2002-nsga-ii]] or [[daulton-2020-qehvi]] can map the full Pareto front.

## Measurement Stability

The MTF score has known bias sources ([[burns-2000-slanted-edge-mtf]]): slope estimation error, discrete derivative filter, image noise. Under identical register settings, scores can fluctuate ±1–3% due to noise. This measurement noise is one reason the CMA-ES step size must not be set too aggressively.

## See also

- [[burns-2000-slanted-edge-mtf]]
- [[multi-objective-optimization]]
- [[Problem_Definition]]
- [[isp-register-optimization]]
- [[cma-es]]
