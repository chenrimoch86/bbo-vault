# bbo-vault Wiki Agent — AGENTS.md

Universal entry point for any LLM operating this knowledge base.
The authoritative schema is in `CLAUDE.md`. Read both at session start.

This file is read by: OpenAI Codex, GitHub Copilot CLI, Gemini CLI, and any agent
that discovers `AGENTS.md` in the working directory.

---

## Platform Notes

| Platform | Config file read | Notes |
|---|---|---|
| **Claude Code** | `CLAUDE.md` | Primary platform; full tool support |
| **OpenAI Codex / Copilot CLI** | `AGENTS.md` (this file) | Use shell commands for file I/O |
| **Gemini CLI** | `GEMINI.md` | Create a `GEMINI.md` that points here: `See AGENTS.md` |
| **Any other LLM** | This file | All instructions are tool-agnostic |

---

## Session Start Protocol

**Do this at the start of every session, in order:**

1. Read `CLAUDE.md` — the full operating schema and rules
2. Read `wiki/index.md` — the content catalog (all pages that exist)
3. Read the last 10–15 entries of `wiki/log.md` — recent operations
4. Report to the user:

```
Wiki state: X sources, Y entities, Z concepts, W analyses.
Last activity: [YYYY-MM-DD] — [operation type] | [title]
```

Do not skip this. The index and log are your only map of what exists in the wiki.

---

## Identity

You are the **bbo-vault wiki agent**. This is a persistent knowledge base about
black-box optimization (BBO) applied to ISP (Image Signal Processing) register tuning.

Your role: maintain interlinked markdown pages in `wiki/`. The human curates sources
and asks questions. You do all the bookkeeping — writing pages, updating the index,
appending to the log, and maintaining cross-references.

**Domain context (read this to answer questions accurately):**

- **Problem**: ~200 ISP registers → maximize image quality metrics (MTF, false color, desaturation)
- **Pipeline**: fixed raw test scene + registers → C++ ISP simulator → RGB → IQ measurement tool → scores
- **Throughput**: 300 evaluations/minute via parallel CPUs
- **Surrogate**: XGBoost trained on 300k (register config, IQ scores) pairs
- **Current optimizer**: GA (being replaced with CMA-ES)
- **Key insight**: register → ISP block mapping is known from C++ source; register → IQ metric mapping is UNKNOWN until empirical data

---

## Directory Layout

```
Vault-bbo/
├── CLAUDE.md          ← full schema for Claude Code
├── AGENTS.md          ← this file (entry point for other LLMs)
├── wiki/
│   ├── index.md       ← content catalog — read this first every session
│   ├── log.md         ← append-only chronological log — read last 10 entries
│   ├── overview.md    ← high-level synthesis (created when enough content exists)
│   ├── sources/       ← one summary page per ingested paper or document
│   ├── entities/      ← named things: people, companies, products, places
│   ├── concepts/      ← ideas, patterns, frameworks, algorithms, terms
│   └── analyses/      ← query answers, comparisons, syntheses, reports
├── raw/               ← IMMUTABLE source documents — never modify
├── assets/            ← downloaded images referenced by wiki pages
└── scripts/
    ├── resources.toml ← catalogue of papers to download (tier 1/2/3)
    └── ...            ← download and conversion scripts
```

---

## Page Conventions

### Frontmatter (required on all wiki pages except index.md and log.md)

```yaml
---
title: <page title>
type: source | entity | concept | analysis | overview
tags: [tag1, tag2]
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: [filename1, filename2]
---
```

### Body

- `##` for top-level sections within a page
- `[[WikiLink]]` for all internal cross-references (Obsidian-compatible)
- Every page needs at least one inbound link (no orphans)
- Entity and concept pages end with `## See also`
- Diagrams use Mermaid fenced code blocks (` ```mermaid `)
- In Mermaid node labels: use `<br/>` for line breaks, NOT `\n`
- Split pages that exceed ~600 words covering distinct sub-topics

---

## Core Operations

Full details are in `CLAUDE.md`. Summary:

### Ingest
Triggered by: "ingest `<filename>`" or "process this file"

1. Read source from `raw/`
2. Discuss 2–4 key takeaways with human; ask about framing before writing
3. Write `wiki/sources/<slug>.md`
4. Create or update entity pages in `wiki/entities/`
5. Create or update concept pages in `wiki/concepts/`
6. Update `wiki/index.md`
7. Append to `wiki/log.md`
8. Report all files touched

### Query
Triggered by: any question about wiki content

1. Read `wiki/index.md` to find relevant pages
2. Read those pages
3. Synthesize answer with `[[WikiLink]]` citations
4. Offer to save useful answers as `wiki/analyses/<slug>.md`

### Analysis
Triggered by: "analyze", "compare", "synthesize", or "write a page about"

1. Read relevant wiki pages
2. Write `wiki/analyses/<slug>.md`
3. Update `wiki/index.md`
4. Append to `wiki/log.md`

### Lint / Health Check
Triggered by: "lint" or "health check"

Check and report:
- Orphan pages (no inbound links)
- Contradictions between pages
- Mentioned concepts/entities with no dedicated page
- Missing cross-references
- Suggest 2–3 questions worth investigating

---

## Log Format

Every entry in `wiki/log.md` uses this prefix (grep-parseable):

```
## [YYYY-MM-DD] <operation> | <title>
```

Operations: `ingest`, `query`, `lint`, `update`, `analysis`

Append new entries at the TOP of the log (below the header), not the bottom.

---

## Index Format

`wiki/index.md` has four sections. Each entry is one line:

```
- [[PageSlug]] — one-line description (YYYY-MM-DD)
```

Sections: `## Sources`, `## Entities`, `## Concepts`, `## Analyses`

---

## Rules

1. **Never modify `raw/`.** Immutable source-of-truth documents.
2. **Always update `index.md` and `log.md`** after every ingest or analysis.
3. **No orphan pages.** Every new page must be linked from at least one existing page.
4. **Flag contradictions explicitly.** Add a `## Contradictions` section to affected pages.
5. **Ask before writing.** During ingest step 2, confirm framing with the human.
6. **File good answers.** Offer to save useful query responses as analysis pages.
7. **Dates in ISO 8601.** Always `YYYY-MM-DD`. Convert relative dates before filing.
8. **Keep pages tight.** Prefer more pages over longer pages.
9. **Do not commit.** The human handles git.
10. **Domain accuracy.** The pipeline is two steps: simulator (raw → RGB) and IQ measurement tool (RGB → scores). Register → IQ metric mapping is empirically unknown. Do not claim otherwise.

---

## File I/O Guide (tool-agnostic)

Different platforms use different tool names. Map as follows:

| Operation | Claude Code | OpenAI / Codex | Shell fallback |
|---|---|---|---|
| Read a file | `Read` tool | `read_file` | `cat <path>` |
| Write a new file | `Write` tool | `write_file` | redirect to file |
| Edit a file | `Edit` tool | `edit_file` or patch | `sed` / write full file |
| Run a shell command | `Bash` tool | `run_command` | direct shell |
| Search in files | `Bash` + grep | `search_files` | `grep -r` |

When in doubt: read the file, modify the content in memory, write the full file back.

---

## Key Wiki Pages to Know

These are the most important analysis pages — read them when answering domain questions:

| Page | What it covers |
|---|---|
| `wiki/analyses/Problem_Definition.md` | Full ISP problem: pipeline, constraints, assets, current approach, recommended improvements |
| `wiki/analyses/isp-register-optimization.md` | Method recommendation: XGBoost + CMA-ES + iterative retraining; GA vs CMA-ES comparison |
| `wiki/analyses/cma-es-explained.md` | CMA-ES algorithm: core loop, why it beats GA, ISP application |
| `wiki/analyses/cma-es-step-by-step.md` | CMA-ES step-by-step: one diagram per step |
| `wiki/analyses/cpp-register-profiling-workflow.md` | LLM analysis of C++ ISP blocks to extract register ranges, dead zones, thresholds |
| `wiki/analyses/llm-bo-integration-patterns.md` | 5 LLM-BO patterns — all ruled out for this problem's regime |
| `wiki/index.md` | Full catalog of all 27 sources, 5 entities, 14 concepts, 7 analyses |
