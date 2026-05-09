---
title: "Active Learning Literature Survey (Settles, 2009)"
type: source
tags: [active-learning, query-by-committee, uncertainty-sampling, pool-based, adaptive-sampling]
created: 2026-05-10
updated: 2026-05-10
sources: [Settles-2009-Active-Learning-Survey.md]
---

**Author**: Burr Settles (University of Wisconsin–Madison)
**Year**: 2009 (updated Jan 2010)
**Type**: Technical Report 1648
**URL**: burrsettles.com/pub/settles.activelearning.pdf

## Summary

Comprehensive survey of active learning — the paradigm where a learner selects which data points to label in order to maximize accuracy with fewer labels. Covers three query scenarios, six strategy frameworks, theoretical analysis, and practical considerations. The ISP validation→disagreement→targeted resampling loop described in [[isp-register-optimization]] is an instance of **query-by-committee active learning** in the pool-based setting.

## Three Scenarios

| Scenario | Setup | ISP Analog |
|----------|-------|-----------|
| Membership query synthesis | Learner generates arbitrary queries | CMA-ES sampling new register configs |
| Stream-based selective sampling | Learner sees one point at a time and decides to label or skip | N/A |
| **Pool-based sampling** | Large unlabeled pool; learner picks which to label | XGBoost proposes top-K; ISP simulator labels them |

## Six Query Strategy Frameworks

1. **Uncertainty sampling**: query the point the model is least certain about (max entropy, min margin, max least-confident)
2. **Query-by-committee (QBC)**: train committee of models; query where they disagree most
3. **Expected model change**: query point that would change the model most
4. **Expected error reduction**: query point that would reduce generalization error most
5. **Variance reduction**: query point that minimizes output variance
6. **Density-weighted methods**: weight informativeness by how representative a point is

## Connection to ISP Validation Loop

The ISP targeted resampling loop (described in [[isp-register-optimization]]):
1. CMA-ES proposes top-K register configs (surrogate-guided)
2. Run full ISP evaluation (oracle labels them)
3. If XGBoost disagrees with evaluation: sample region around disagreement, run simulator, retrain XGBoost

This is **QBC active learning**: the XGBoost model is the "committee" (implicitly), and the ISP simulator is the oracle. The "disagreement region" corresponds to high prediction error — exactly the Query-by-Committee criterion.

Settles's analysis confirms: QBC active learning reliably improves model accuracy with 30–50% fewer labels than random sampling in typical cases.

## Batch-Mode Active Learning

For practical use, batch-mode active learning (querying b points per round, Section 6.1) is more efficient than sequential queries because:
- The ISP simulator runs 300 evals/min in parallel — batches make sense
- Single sequential queries waste parallelism

Suggested approach: use the QBC criterion to identify the top-b most informative configs in the disagreement region, run them in parallel, retrain XGBoost once.

## See also

- [[active-learning]]
- [[isp-register-optimization]]
- [[surrogate-model]]
- [[chen-2016-xgboost]]
