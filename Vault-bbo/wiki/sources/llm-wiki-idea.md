---
title: LLM Wiki — The Core Idea
type: source
tags: [knowledge-management, llm, wiki, rag]
created: 2026-05-08
updated: 2026-05-08
sources: [example-llm-wiki-idea.md]
---

# LLM Wiki — The Core Idea

A pattern for building personal knowledge bases where an LLM incrementally builds and maintains a persistent wiki, rather than re-deriving answers from raw documents on every query (RAG).

## Core argument

Standard RAG re-discovers knowledge from scratch on every question. The LLM Wiki pattern compiles knowledge once into a persistent, interlinked wiki and then *keeps it current*. Cross-references are pre-built. Contradictions are pre-flagged. The synthesis already reflects everything ingested.

## How it works

1. Human drops a source into `raw/`.
2. LLM reads it, discusses key takeaways, then integrates: writes a summary page, updates entity pages, updates concept pages, flags any contradictions with prior content.
3. The wiki grows richer with every source. Queries read the pre-synthesized wiki rather than raw documents.

## The human/LLM division of labor

- **Human**: curates sources, asks questions, directs analysis.
- **LLM**: writes and maintains all wiki pages — summaries, cross-references, entity pages, contradiction flags.

The wiki fails when humans have to do the bookkeeping. LLMs handle bookkeeping at near-zero cost.

## Spiritual predecessor

[[Vannevar Bush]]'s [[Memex]] (1945) — a personal, curated knowledge store with associative trails between documents. The missing piece was who does the maintenance. The LLM solves that.

## Tooling

- [[Obsidian]] — markdown editor, graph view, plugin ecosystem
- [[qmd]] — local hybrid BM25/vector search engine for markdown (CLI + MCP server)
- Obsidian Web Clipper, Marp, Dataview

## See also

- [[RAG]] — the pattern this improves on
- [[Compounding Knowledge]] — the key property the wiki provides
- [[Schema File]] — what makes the LLM a disciplined wiki agent
- [[Vannevar Bush]] — intellectual ancestor
