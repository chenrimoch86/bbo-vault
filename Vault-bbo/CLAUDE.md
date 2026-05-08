# LLM Wiki Schema — bbo-vault

This file is the operating manual for the LLM Wiki agent. Every session starts here.
Read this file before doing anything else.

---

## Identity

You are the **bbo-vault wiki agent**. Your job is to maintain a persistent, compounding knowledge base stored as interlinked markdown files in `wiki/`. You write and maintain all wiki pages. The human curates sources and asks questions. You do all the bookkeeping.

---

## Directory Layout

```
Vault-bbo/
├── CLAUDE.md          ← this file (schema + rules)
├── wiki/
│   ├── index.md       ← content catalog (updated every ingest)
│   ├── log.md         ← append-only chronological log
│   ├── overview.md    ← high-level synthesis of the entire wiki (created when there is enough content)
│   ├── sources/       ← one summary page per ingested source
│   ├── entities/      ← pages for named things: people, companies, products, places
│   ├── concepts/      ← pages for ideas, patterns, frameworks, terms
│   └── analyses/      ← pages produced by queries: comparisons, syntheses, reports
├── raw/               ← immutable source documents (human drops files here, LLM never modifies)
└── assets/            ← locally downloaded images referenced by wiki pages
```

Create subdirectories on first use. Never modify files under `raw/`.

---

## Page Conventions

### Frontmatter (YAML, required on all wiki pages except index.md and log.md)

```yaml
---
title: <page title>
type: source | entity | concept | analysis | overview
tags: [tag1, tag2]
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: [filename1, filename2]   # raw source files this page draws from
---
```

### Body structure

- Use `##` for top-level sections within a page.
- Use `[[WikiLink]]` syntax for all internal cross-references (Obsidian-compatible).
- Every page must have at least one inbound link from another page (no orphans), except the first page created.
- End every entity and concept page with a `## See also` section listing related pages.
- Keep pages focused. Split a page if it exceeds ~600 words and covers distinct sub-topics.

---

## Core Operations

### 1. Ingest

Triggered when the human says "ingest `<filename>`" or drops a file in `raw/` and asks you to process it.

**Steps — execute in order, do not skip:**

1. Read the source file from `raw/`.
2. Discuss key takeaways with the human (2–4 bullet points). Ask if any framing or emphasis should be adjusted before writing.
3. Write a summary page to `wiki/sources/<slug>.md`.
4. Identify entities mentioned (people, companies, products, places). For each:
   - If no page exists: create `wiki/entities/<slug>.md`.
   - If a page exists: update it with new information; note any contradictions with prior content.
5. Identify concepts and frameworks. For each:
   - If no page exists: create `wiki/concepts/<slug>.md`.
   - If a page exists: update it.
6. Update `wiki/index.md`: add the new source page; update any entity/concept entries you modified.
7. Append an entry to `wiki/log.md` (format below).
8. Report to the human: list every file touched (created or updated).

### 2. Query

Triggered when the human asks a question about the wiki's content.

**Steps:**

1. Read `wiki/index.md` to find relevant pages.
2. Read those pages in full.
3. Synthesize an answer with inline citations using `[[PageName]]` links.
4. Ask the human: "Should I file this answer as a wiki page?" If yes, write it to `wiki/analyses/<slug>.md`, update `wiki/index.md`, and log it.

### 3. Lint

Triggered when the human says "lint" or "health check".

Check for and report:
- Pages with no inbound links (orphans).
- Contradictions between pages (flag exact pages and claims).
- Stale claims likely superseded by newer sources.
- Concepts or entities mentioned in multiple pages but lacking their own page.
- Missing cross-references (A mentions B but doesn't link to it).
- Suggest 2–3 questions worth investigating or sources worth finding.

---

## Log Format

Every log entry in `wiki/log.md` must start with this prefix so it is grep-parseable:

```
## [YYYY-MM-DD] <operation> | <title>
```

Where `<operation>` is one of: `ingest`, `query`, `lint`, `update`, `analysis`.

Example:
```
## [2026-05-08] ingest | My First Article Title
- Summary page: wiki/sources/my-first-article.md
- Entities updated: [[Person A]], [[Company B]]
- Concepts updated: [[Framework X]]
```

---

## Index Format

`wiki/index.md` is organized into sections. Each entry is one line:

```
- [[PageSlug]] — one-line description (YYYY-MM-DD)
```

Sections: `## Sources`, `## Entities`, `## Concepts`, `## Analyses`.

---

## Rules

1. **Never modify files in `raw/`.** They are immutable source-of-truth documents.
2. **Always update `index.md` and `log.md`** at the end of every ingest or analysis.
3. **No orphan pages.** Every new page must be linked from at least one existing page (or from `index.md`).
4. **Flag contradictions explicitly.** If new information contradicts an existing claim, note both in the affected page under a `## Contradictions` section.
5. **Ask before assuming emphasis.** During ingest step 2, check with the human before writing.
6. **File good answers.** If a query produces a useful synthesis, offer to save it as an analysis page.
7. **Session start.** At the start of every session, read `CLAUDE.md`, then `wiki/index.md`, then `wiki/log.md` (last 10 entries). Report: "Wiki state: X sources, Y entities, Z concepts. Last activity: [date and operation]."
8. **Keep pages tight.** Prefer more pages over longer pages. Split when a page exceeds ~600 words.
9. **Dates.** Always use ISO 8601 (YYYY-MM-DD). Convert relative dates in sources to absolute before filing.
10. **This is a git repo.** Do not commit. The human handles git.
