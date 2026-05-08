---
title: Schema File
type: concept
tags: [llm-wiki, configuration, claude]
created: 2026-05-08
updated: 2026-05-08
sources: [example-llm-wiki-idea.md]
---

# Schema File

The configuration document (e.g. `CLAUDE.md` for Claude Code, `AGENTS.md` for Codex) that turns a general-purpose LLM into a disciplined [[LLM Wiki — The Core Idea|wiki agent]].

## What it contains

- Directory layout and file naming conventions
- Page frontmatter format
- Step-by-step workflows for each operation (ingest, query, lint)
- Log format and update rules
- Hard rules (e.g. never modify `raw/`, always update `index.md`)

## Why it's the key piece

Without a schema file, the LLM is a generic chatbot. With it, the LLM knows exactly what to do when you say "ingest this file" — which pages to create, which to update, how to log the operation, and what to report back. The schema makes the behavior reproducible across sessions.

The human and LLM co-evolve the schema over time as the domain and workflow become clearer.

## This wiki's schema

See `CLAUDE.md` in the project root.

## See also

- [[LLM Wiki — The Core Idea]]
- [[Compounding Knowledge]]
