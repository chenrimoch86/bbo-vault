---
title: RAG (Retrieval-Augmented Generation)
type: concept
tags: [llm, retrieval, knowledge-management]
created: 2026-05-08
updated: 2026-05-08
sources: [example-llm-wiki-idea.md]
---

# RAG (Retrieval-Augmented Generation)

The standard LLM pattern for answering questions from a document collection. At query time, relevant chunks are retrieved from a vector index and injected into the prompt; the LLM generates an answer.

## Limitation

No accumulation. The LLM re-discovers knowledge from scratch on every query. Subtle questions that require synthesizing five documents require finding and piecing together those fragments every time. Nothing compounds.

## Contrast with LLM Wiki

The [[LLM Wiki — The Core Idea]] pattern compiles knowledge once into a persistent wiki and keeps it current. By the time you ask a question, the cross-references are already there, the contradictions are already flagged, and the synthesis already exists as a page.

RAG is infrastructure; the LLM Wiki is editorial.

## See also

- [[LLM Wiki — The Core Idea]]
- [[Compounding Knowledge]]
