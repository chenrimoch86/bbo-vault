---
title: "Slanted-Edge MTF for Digital Camera and Scanner Analysis (Burns, 2000)"
type: source
tags: [mtf, image-quality, isp, spatial-frequency-response, iso-12233]
created: 2026-05-10
updated: 2026-05-10
sources: [Burns-2000-Slanted-Edge-MTF.md]
---

**Author**: Peter D. Burns (Eastman Kodak)
**Year**: 2000
**Venue**: IS&T PICS Conference
**URL**: imaging.org/common/uploaded%20files/pdfs/Papers/2000/PICS-0-81/1621.pdf

## Summary

Establishes slanted-edge analysis as the standard method for measuring Modulation Transfer Function (MTF) of digital cameras. Defines the ISO 12233 Spatial Frequency Response (SFR) algorithm, identifies its bias sources, and provides working equations for each. This is the foundational paper for understanding what the MTF score in the ISP pipeline actually measures and where its errors come from.

## What MTF Measures

MTF (Modulation Transfer Function) quantifies how faithfully a system reproduces spatial frequencies — i.e., sharpness at different scales. It is the normalized modulus of the Optical Transfer Function (OTF). A score close to 1.0 at a given frequency means the system accurately reproduces that frequency; degradation toward 0 means blurring.

## The Slanted-Edge Method (ISO 12233)

The ISO 12233 algorithm extracts MTF from a slanted (skewed) edge in the image:

1. Select region of interest (ROI) around the edge
2. Transform image data via OECF (opto-electronic conversion function)
3. Compute luminance from R, G, B channels
4. Estimate edge location and direction via linear fit to derivative centroids
5. Project all pixels along the edge direction → 4× supersampled edge-spread function
6. Apply Hamming window, compute DFT
7. Normalize modulus → SFR (or MTF if corrected for input edge modulation)

The 4× supersampling step is key: it reduces aliasing artifacts in the measured SFR by averaging sub-pixel offsets across many scan lines.

## Bias Sources and Their Effects

| Source | Effect | Direction |
|--------|--------|-----------|
| Slope estimation error (skew MTF) | High-freq attenuation; increases with ROI height m | Negative bias |
| Discrete derivative filter | High-freq attenuation; smaller at 4× oversample | Negative bias |
| Image noise | Random variation + positive offset | Positive bias |
| Color misregistration | Channel-dependent frequency shifts | Varies |

Acceptable results require: edge slope error < 0.5°; SNR > 12.5 (pixel signal-to-noise).

## Relevance to ISP Register Optimization

- The MTF score output by the IQ measurement tool is computed by this algorithm on the fixed test scene chart
- ISP registers affect sharpening, demosaic, and noise reduction blocks — all of which directly shift the MTF curve
- Understanding bias sources explains why MTF scores can fluctuate for identical register settings under noisy conditions
- "MTF" and "SFR" are distinct: SFR is uncorrected, MTF is corrected for input target; most practical tools report SFR under the MTF label

## See also

- [[image-quality-metrics]]
- [[surrogate-model]]
- [[Problem_Definition]]
