---
title: "LLM Agent for Hyper-Parameter Optimization (Wang et al., 2025)"
type: source
tags: [llm, hyperparameter-optimization, uav, mcp, pso]
created: 2026-05-08
updated: 2026-05-08
sources: [Wang-2025-LLM-Agent-HPO.md]
---

**Authors**: Wanzhe Wang et al.
**Affiliation**: Harbin Institute of Technology (Shenzhen) et al.
**Year**: 2025
**URL**: arxiv.org/abs/2506.15167

## Summary

Domain-specific application of an LLM agent (via Model Context Protocol) to tune hyperparameters of the WS-PSO-CM (Warm-Start Particle Swarm Optimization with Crossover and Mutation) algorithm for radio map-enabled UAV trajectory and communication optimization. Demonstrates +54% improvement over human heuristics and +73% over uniform random sampling.

## Key Points

- Uses **Model Context Protocol (MCP)** to structure LLM agent interactions with the WS-PSO-CM algorithm.
- LLM agent profile specifies: hyperparameter bounds, task objective, terminal condition, optimization strategy (conservative vs. aggressive).
- Iterative framework: agent invokes WS-PSO-CM, observes results, proposes new hyperparameters.
- Illustrates MCP as a general tooling pattern for LLM-driven HPO in domain-specific settings.

## See also

- [[llm-bo-hybrid]]
- [[hyperparameter-optimization]]
