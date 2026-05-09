---
title: "Active Learning"
type: concept
tags: [active-learning, query-by-committee, adaptive-sampling, surrogate-retraining, oracle]
created: 2026-05-10
updated: 2026-05-10
sources: [Settles-2009-Active-Learning-Survey.md]
---

Active learning is the paradigm where a learner *selects* which data points to label in order to improve a model faster than passive random sampling. A key idea: with limited labeling budget, choose the points that will teach the model the most.

In the ISP context: the ISP simulator is the "oracle" (expensive to run), the XGBoost model is the "learner," and choosing which register configurations to evaluate is the active learning problem.

## Key Scenarios

**Pool-based sampling** (most relevant to ISP): A large pool of unlabeled candidates exists; the learner selects which to label. For ISP: CMA-ES proposes top-K candidates; the question is which of those K to actually run through the simulator.

## Query Strategies

### Uncertainty Sampling
Label the point the current model is least confident about. For regression: highest prediction variance.

### Query-by-Committee (QBC)
Train multiple models (the "committee"); label where they disagree most. For ISP: the "committee" is effectively the XGBoost model vs. the true ISP simulator. Disagreement = high prediction error.

**The ISP validation loop is QBC active learning:**
1. XGBoost predicts IQ scores for top-K CMA-ES candidates
2. Run top-K through ISP simulator (oracle)
3. Find where |XGBoost prediction - simulator output| is large (disagreement)
4. Sample more points in that region, run simulator, retrain XGBoost
5. Repeat → surrogate improves specifically in the optimizer-relevant region

### Expected Error Reduction
Label the point that, if added to training, would most reduce model generalization error. More principled than QBC but computationally expensive.

## Batch Active Learning

Since the ISP simulator runs 300 evals/min in parallel, batch selection is essential: choose b points per round rather than one. Good batch strategies avoid redundancy (selecting b similar points wastes budget) by distributing queries across the disagreement region.

## Theoretical Guarantee (from Settles survey)

For QBC with a consistent hypothesis class, active learning achieves the same error with exponentially fewer labels than passive learning (in favorable cases). In practice, 30–50% label reduction is typical.

## Connection to Targeted Retraining in ISP

The [[isp-register-optimization]] analysis describes a "targeted resampling" step: when XGBoost disagrees with the simulator on top-K candidates, sample 2–5k points in that region and retrain. This is precisely QBC batch active learning, and Settles's survey provides the theoretical backing for why this strategy reliably improves surrogate accuracy in the optimizer-relevant region faster than random resampling.

## See also

- [[settles-2009-active-learning]]
- [[isp-register-optimization]]
- [[surrogate-model]]
- [[chen-2016-xgboost]]
- [[metamodel-validation]]
