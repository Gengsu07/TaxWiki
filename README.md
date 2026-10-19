# TaxWiki — Indonesian Tax Wiki

A personal knowledge base for **Indonesian tax law** (UU, PMK, PP, SE, and related rules), powered by AI agents and based on [Andrej Karpathy's LLM Wiki pattern](llm-wiki.md). The AI agent builds and maintains a structured, interlinked wiki of markdown files. You curate sources and ask questions — the agent does all the bookkeeping.

> **Architecture note**: Read [TAXWIKIDESIGN.md](TAXWIKIDESIGN.md) first for the goals, design decisions, and the fine-tuning pipeline. This README covers daily usage.

> **Do not use real taxpayer data.** TaxWiki is for concepts, methods, and fictional use cases only — not SPT, NPWP, or client files. See [PRIVACY.md](PRIVACY.md) and [TERMS.md](TERMS.md).

## Philosophy

Most RAG systems rediscover knowledge on every query. TaxWiki is different: **knowledge compounds**. When you add a source (a new PMK, an article on PPh 21, a court decision), the agent reads it, extracts the key ideas, creates concept pages, cross-references related pages, and flags contradictions. The wiki gets richer with every source and every question. Answers are filed back as new pages so nothing is lost.

Every ingest also **accumulates training data for free** — the source→page pairs become the fine-tuning dataset for a small local model (`dataset/`, see below). Eventually the wiki answers questions fully offline on weak hardware.

> **Obsidian is the IDE. The AI agent is the programmer. The wiki is the codebase.**

## Structure

```
TaxWiki/
├── raw/                    # Immutable tax sources (never modified)
│   ├── assets/             # Downloaded images and attachments
│   ├── UU NO 6 2023-*.md   # Undang-Undang (laws)
│   ├── PPh 21/  PPN/       # Topic folders: PMK, articles
│   └── UMKM/  Sanksi Administrasi/  Jasa Konstruksi/ ...
├── wiki/                   # Agent-maintained markdown pages
│   ├── index.md            # Table of contents for the entire wiki
│   ├── log.md              # Append-only record of all operations
│   ├── concept/            # Concept pages grouped into chapter folders
│   └── embeddings/         # Exported chunk JSONL snapshots (committed)
├── dataset/                # Fine-tuning data pipeline (see dataset/README.md)
│   ├── qa-raw/             # Q&A pairs written by the agent during ingest
│   └── task-*.jsonl        # Generated training samples (committed)
├── tools/make-dataset.py   # Mines raw/ + wiki/ into Unsloth-ready JSONL
├── .agents/                # Shared agent skills (pi / Claude Code / OpenCode)
├── TAXWIKIDESIGN.md        # Architecture + decisions record
├── AGENTS.md               # Agent schema — workflows and conventions
├── llm-wiki.md             # Karpathy's original idea document
└── README.md               # This file
```

*`.knowledge/`* (the pi-knowledge binary search index) and downloaded model weights are
gitignored — they are disposable caches rebuilt from committed JSONL.

## Getting Started

### 1. Clone and open in Obsidian

```bash
git clone https://github.com/Gengsu07/TaxWiki.git
# Open the TaxWiki folder as an Obsidian vault
```

Obsidian provides graph view, [[wikilink]] navigation, and a Dataview-based Bases plugin for dynamic views.

### 2. Add your first source

Drop tax documents into `raw/` — laws (UU), regulations (PMK, PP), articles, court decisions — as markdown or PDF.

### 3. Tell the agent to ingest

Open your AI agent (pi, OpenCode, Claude Code) in the TaxWiki directory and say:

> "Ingest the source in raw/UMKM/Riwayat Perubahan Aturan PPh UMKM PP 46, PP23, PP55.md"

The agent will:
1. Read the source and discuss key takeaways with you
2. Create a summary page in `wiki/`
3. Create or update concept pages for each major idea, classified into chapter folders
4. Link related pages with [[wikilinks]]
5. Update `wiki/index.md`, `wiki/log.md`, and the chapter learning paths
6. Write 5–10 grounded Q&A pairs to `dataset/qa-raw/` (accumulates training data)
7. Run `python tools/make-dataset.py` to refresh the training JSONL

### 4. Query the wiki

> "Berapa tarif PPh final UMKM menurut PP 23 Tahun 2018?"

The agent reads the index, finds relevant pages, and synthesizes an answer with citations. Good answers get saved back as new pages.

### 5. Semantic search (optional but recommended)

Index the wiki with pi-knowledge (stored in `.knowledge/`, gitignored):

```bash
# once: pi install -l npm:pi-knowledge
# launch pi with the KB inside the repo (see TAXWIKIDESIGN.md §6)
$env:PI_KNOWLEDGE_DIR = "$PSScriptRoot\.knowledge"

knowledge_add raw/ "Indonesian Tax Wiki"
knowledge_search "tarif PPh badan"
knowledge_export "Indonesian Tax Wiki" wiki/embeddings/indonesian-tax-wiki.jsonl
```

Hybrid BM25 + multilingual-e5 vector search runs fully local — no API keys.

## Daily Workflows

### Ingesting sources

Drop a file into `raw/` → tell the agent to ingest it → review the changes in Obsidian's graph view. One source typically touches 10-15 wiki pages **and adds 15–30 training samples**.

### Asking questions

Ask anything against the wiki. The agent searches, synthesizes, and files valuable answers as new pages. Cross-topic questions benefit from the graphify knowledge graph.

### Linting / auditing

> "Lint the wiki"

The agent checks for contradictions, orphan pages, missing concept pages, stale claims, and format compliance. **The lint pass is also data cleaning** — only `status: stable` pages become training data.

### Fine-tuning the small model

The wiki accumulates its own dataset. At ~30 ingested sources (~450–900 samples), fine-tune Phi-4-mini on RunPod/Colab and run it locally via Ollama on 8GB hardware. Full runbook: [dataset/README.md](dataset/README.md).

### Browsing visually

- **Obsidian graph view** — see the shape of your knowledge: hubs, clusters, orphans
- **.base views** — filterable tables and card views over all pages
- **graphify knowledge graph** — community-detected clusters, hidden connections
- **Canvas files** — visual mind maps of related concepts

## Available Skills

The agent is equipped with specialized skills that enhance wiki maintenance:

### Core wiki skills

| Skill | Purpose |
|-------|---------|
| `obsidian-markdown` | Write Obsidian-compatible [[wikilinks]], callouts, frontmatter, and embeds |
| `obsidian-bases` | Create `.base` files for database-like tables, cards, and filtered views |
| `obsidian-json-canvas` | Create visual mind maps and concept diagrams (`.canvas` files) |
| `obsidian-cli` | Automate Obsidian — create notes, search, manage properties from CLI |

### Knowledge graph

| Skill | Purpose |
|-------|---------|
| `graphify` | Build a knowledge graph from wiki content — detect communities, find hidden connections, query relationships between concepts |

### Source ingestion

| Skill | Purpose |
|-------|---------|
| `obsidian-defuddle` | Extract clean markdown from web articles (replaces WebFetch for most URLs) |

### Output formats

| Skill | Purpose |
|-------|---------|
| `slides` | Generate HTML slide presentations from wiki content |
| `brainstorming` | Interactive visual tool for exploring ideas before writing |
| `interactive-explainer` | Create animated HTML explainers for complex concepts |
| `pdf` | Read and extract content from PDF sources |
| `docx` | Read and edit Word documents |
| `pptx` | Create and edit PowerPoint presentations |
| `xlsx` | Work with spreadsheets |

## Key Concepts

### wiki/index.md

The table of contents. Lists every page with a one-line description and metadata. The agent reads this first when answering queries. Updated on every ingest.

### wiki/log.md

An append-only timeline. Every operation (ingests, queries, lint passes) gets an entry with date and summary. Parseable with `grep "^## \[" log.md | tail -5`.

### Concept pages

Each major tax concept gets its own page in `wiki/concept/<chapter>/`. Pages include YAML frontmatter (title, tags, date, sources, status, chapter) for Dataview/Bases compatibility. They link to related concepts with [[wikilinks]] and cite sources as `(source: filename.md)`.

### Obsidian Bases

`.base` files provide filterable database views. Example uses:
- **Source inventory**: table of all ingested sources with dates and tags
- **Concept index**: card view of all concepts grouped by chapter
- **Lint dashboard**: filter to pages with `status: draft`

### Dataset accumulation

`tools/make-dataset.py` turns the wiki itself into training data: page-write, summarize, and classify samples plus Q&A pairs. Deterministic and incremental — re-run after every ingest batch and commit the JSONL. See [dataset/README.md](dataset/README.md).

## Customization

TaxWiki is designed to evolve with you:

- **Change the page format** — edit the template in `AGENTS.md`
- **Add new workflows** — write them into `AGENTS.md` and the agent follows them
- **Add new dataset task types** — extend `tools/make-dataset.py` (one sample = one scoped subtask)
- **Install more skills** — add skill folders to `.agents/`
- **Adjust the structure** — add subdirectories to `wiki/` for new page types
- **Co-evolve the schema** — refine `AGENTS.md` as you learn what works
- **Change the architecture** — update `TAXWIKIDESIGN.md` alongside the change

## Credits

Based on [Andrej Karpathy's LLM Wiki](llm-wiki.md) pattern. The core insight: LLMs don't get bored and can maintain cross-references across hundreds of pages, solving the maintenance burden that kills human-maintained wikis.
