---
title: "Memory-Guided TuRBO (MG-TuRBO, 2026)"
type: source
tags: [trust-region, bayesian-optimization, restart-strategy, traffic-simulation, high-dimensional]
created: 2026-05-08
updated: 2026-05-08
sources: [MG-TuRBO-2026.md]
---

**Year**: 2026
**Application domain**: Traffic simulation calibration

## Summary

MG-TuRBO extends [[trust-region-bo]] with **memory-guided restarts**: instead of initializing new trust regions randomly after collapse, it clusters the full evaluation history into basins and selects restart centers from basins that are both high-quality (good function values) and underexplored (low visitation count). This retains the local-BO efficiency of TuRBO while providing more intelligent global exploration over the course of an optimization run.

## Methodology

**Basin Clustering**
- All evaluated points in the normalized design space are clustered (e.g., k-means) into basins.
- Each basin is assigned: (1) a quality score based on the best observation within it, and (2) a visitation count.

**Guided Restart Selection**
- When a TR collapses (L < L_min), select a restart center from a basin with high quality and low visitation — promising but underexplored.
- This biases the search toward unexploited regions of the design space that have shown some promise.

**Adaptive Acquisition**
- Uses a weighted combination of improvement and uncertainty in the acquisition function, adapting the balance based on optimization progress.

## Results

Applied to traffic simulation calibration using SUMO (Simulation of Urban Mobility):
- **14D** (Shallowford Road corridor, Chattanooga, TN)
- **84D** (Murfreesboro Pike corridor, Nashville, TN)

MG-TuRBO shows clear advantages at 84D compared to genetic algorithm (GA) and standard TuRBO, where the memory-guided restarts prevent premature convergence.

## See also

- [[trust-region-bo]]
- [[eriksson-2019-turbo]]
- [[high-dimensional-bo]]
- [[bayesian-optimization]]
