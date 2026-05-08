---
title: Compounding Knowledge
type: concept
tags: [knowledge-management, llm-wiki]
created: 2026-05-08
updated: 2026-05-08
sources: [example-llm-wiki-idea.md]
---

# Compounding Knowledge

The property of a [[LLM Wiki — The Core Idea|LLM Wiki]] where each new source makes the entire knowledge base more valuable, not just by adding new content but by enriching existing pages with new connections and context.

## Mechanism

1. New source arrives.
2. LLM reads it and updates not just a summary page, but all relevant entity and concept pages.
3. Cross-references are added, contradictions noted, syntheses updated.
4. Future queries benefit from the accumulated synthesis — not just the latest source.

## Why it matters

In RAG, the value of your knowledge base grows linearly with the number of documents (more to retrieve from). In a compounding wiki, value grows super-linearly because every new source can reinforce, contradict, or extend existing pages — building density and reliability in the core concepts over time.

## See also

- [[LLM Wiki — The Core Idea]]
- [[RAG]]
- [[Schema File]]
