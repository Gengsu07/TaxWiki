# TAXWIKIDESIGN — Indonesian Tax Wiki: Goals & Architecture

> **Read this first.** Authoritative design record for this repo. Written 2026-08-18
> after the architecture discussion with the owner. For any future LLM/agent working
> here: this explains *why* things are the way they are, not just *what* they are.
> Companion docs: `AGENTS.md` (wiki operating rules), `dataset/README.md` (fine-tuning
> pipeline runbook), `llm-wiki.md` (the underlying LLM Wiki pattern).

---

## 1. Goal

Transform this repo into an **Indonesian Tax Wiki** that:

1. Follows the LLM Wiki pattern (`raw/` sources → LLM-maintained `wiki/` pages).
2. Has **semantic search** over sources + pages (hybrid BM25 + vector).
3. **Accumulates its own fine-tuning dataset** for free, from normal use.
4. Eventually runs fully offline on **weak hardware** (8GB RAM, no discrete GPU):
   - a small fine-tuned model (Phi-4-mini class) for daily Q&A + page edits,
   - a strong cloud model (currently `glm-5.1`) for heavy ingests.
5. Stays **portable and git-versioned**: knowledge survives cloning; no dependence
   on `~/.pi` or any single machine.

## 2. Architecture overview

```
raw/                     immutable source docs (UU, PMK, SE, articles)  [committed]
   │  ingest (strong model) — one source touches 10-15 pages
   ▼
wiki/                    compiled knowledge: summary + concept pages   [committed]
   │  tools/make-dataset.py mines (raw → page) gold pairs
   ▼
dataset/                 training data (ShareGPT JSONL)                [committed]
   │  RunPod/Colab: dataset/train.py (Unsloth LoRA, 1 epoch)
   ▼
GGUF (~2.7GB)            fine-tuned small model  → Ollama on laptop    [gitignored]
```

**Search layer** (separate axis):
```
raw/ + wiki/
   │  knowledge_add (PI_KNOWLEDGE_DIR=.knowledge)
   ▼
.knowledge/              SQLite + vectors + model cache               [gitignored]
   │  knowledge_search: hybrid BM25 + multilingual-e5 vectors (+ reranker)
   ▼
answer with (source: file) citations
```

## 3. Key decisions (with rationale)

0. **KB source scopes & exclusions.** Two KBs: "Indonesian Tax Wiki" <- `raw/`,
   "TaxWiki Wiki Pages" <- `wiki/` with `exclude_paths: ["log.md"]` (append-only
   ops history adds search noise; recreated via remove+add when the exclude list
   changes, since `knowledge_update` only refreshes the retained source).

1. **The wiki pages ARE the primary knowledge store.** Compiled once at ingest,
   not re-derived per query (Karpathy pattern). RAG augments, doesn't replace.

2. **`.knowledge/` holds pi-knowledge's binary index, gitignored.** It is a
   disposable cache. Rebuilt anytime with `knowledge_import` from exported JSONL.
   - Relocate with env var **`PI_KNOWLEDGE_DIR`** (verified in pi-knowledge source:
     `getDefaultKnowledgeDir()` checks it first). Pi does **not** auto-load `.env`;
     set it before launching the agent (launcher script or shell profile).
   - `knowledge_export` writes **text chunks + metadata only (no vectors)** —
     git-friendly JSONL; `knowledge_import` re-embeds on any machine.
   - Export convention: `dataset/embeddings/<kb>.jsonl`. **Never export into
     `wiki/`** — pi-knowledge indexes the whole `wiki/` directory, so a snapshot
     inside it gets re-indexed into the wiki KB (feedback loop: 92% of chunks
     became quoted JSON; fixed 2026-08-24).
   - Embedding model: `local:multilingual-e5-small` — free, CPU-only, good
     Indonesian. Reranker: MiniLM. No API keys, no per-query cost.
   - `knowledge_update` is **incremental by content hash** — unchanged chunks
     reuse vectors, only new/changed text gets embedded.

3. **Fine-tuning teaches behavior, RAG provides facts — never the reverse.**
   A 3.8B model cannot hold the tax code, and must not try: laws change, numbers
   must be exact, and AGENTS.md requires `(source: filename)` citations that only
   retrieved context can supply. The QA training samples deliberately teach
   *grounding discipline* ("answer ONLY from context, cite, else say you don't
   know"), not fact memorization. Partial memorization is worse than none.

4. **One dataset sample = one scoped subtask.** Never train the full 15-file
   ingest cascade — that is long-horizon planning, which small models can't learn
   from SFT. Task types per page: `page-write` (short sources only, ≤10k chars),
   `summarize`, `classify`; plus `qa` pairs from `dataset/qa-raw/`.

5. **Dataset grows incrementally, deterministically.** Re-run
   `python tools/make-dataset.py` after every ingest batch. Sample identity and
   the ~10% eval split are hashed per source → re-runs only append; train/eval
   assignment stays stable; git diffs stay minimal.

6. **Quality gate: only `status: stable` (or `review`) pages become training data.**
   Draft pages would teach format errors. The lint pass doubles as data cleaning.

7. **Long laws are the richest dataset sources** — via the many concept pages and
   QA pairs they generate (~60–220 samples per UU), not via page-write (too long,
   and correctly so). Optional v2: `excerpt-raw/` pairs (law excerpt → page
   section) to add excerpt-level authoring samples.

8. **Training runs in the cloud (RunPod/Colab, NVIDIA GPU required); inference
   runs locally.** Unsloth needs CUDA — the 8GB laptop cannot train. Default:
   `unsloth/Phi-4-mini-instruct`, 4-bit, LoRA r=16, **1 epoch**, lr 2e-4,
   max_seq_length 4096 → export GGUF `q4_k_m` → Ollama. 30–60 min on L4/A10,
   <$1 spot. "Several hours" of training = overfitting, not quality.

9. **pi-knowledge installed per-project**: `pi install -l npm:pi-knowledge`
   writes to `.pi/settings.json`, packages under `.pi/npm/` (already gitignored),
   auto-installed on startup for anyone who clones + trusts the repo.

## 4. Model strategy per hardware tier

| Tier | Hardware | Chat model | Role |
|------|----------|------------|------|
| Office laptop | 8GB RAM, no GPU | Fine-tuned **Phi-4-mini (3.8B)** Q4 via Ollama | daily Q&A, single-page edits |
| Owner machine | 16GB, RTX 2060 | Qwen2.5-14B / current glm-5.1 | heavy ingest, dataset QA generation |
| Cloud (RunPod/Colab) | T4/L4+ | — (training only) | LoRA fine-tune + GGUF export |

- Embeddings (multilingual-e5-small) and reranker (MiniLM) are already local and
  CPU-friendly on all tiers — no change ever needed there.
- Alternatives: Gemma 3 4B, Qwen2.5-3B. Existing Indonesian finetunes
  (e.g. SahabatAI) should be tried **before** fine-tuning our own.
- Cheaper levers first: zero-shot → few-shot examples in AGENTS.md → existing
  models → fine-tune last.

## 5. Data volume guidance (when to train)

| Sources ingested | Samples (est.) | Readiness |
|------------------|----------------|-----------|
| ~10 | 150–300 | minimum, expect drift |
| **~30** | 450–900 | **first training run** |
| 50–60 | 1,000–1,500 | sweet spot; plateau beyond |

- Quality > quantity (LIMA: 1k curated beats 50k noisy).
- Retrain on a **data trigger** (+100–200 new samples or visible format drift),
  never on a schedule.
- Vary system-prompt phrasing once ~500 samples are reached (avoid rote memorization).

## 6. Key commands

```bash
# per-project knowledge tooling (once)
pi install -l npm:pi-knowledge

# launch pi with the KB inside the repo (or set PI_KNOWLEDGE_DIR in shell profile)
$env:PI_KNOWLEDGE_DIR = "$PSScriptRoot\.knowledge"   # launch-pi.ps1

# index / update / search
knowledge_add raw/ "Indonesian Tax Wiki"
knowledge_update "Indonesian Tax Wiki"          # incremental, hash-based
knowledge_search "tarif PPh badan"              # hybrid BM25+semantic

# export portable snapshot (commit it)
knowledge_export "Indonesian Tax Wiki" wiki/embeddings/indonesian-tax-wiki.jsonl

# dataset refresh after every ingest batch (commit the JSONL)
python tools/make-dataset.py

# training (RunPod/Colab GPU)
python dataset/train.py --export-gguf
```

## 7. File inventory

| Path | Purpose |
|------|---------|
| `TAXWIKIDESIGN.md` | this document |
| `AGENTS.md` | wiki operating rules; ingest steps 11–12 = dataset accumulation |
| `tools/make-dataset.py` | mines `raw/`+`wiki/` → `dataset/*.jsonl` (3 task types + QA merge) |
| `dataset/qa-raw/*.jsonl` | Q&A pairs written by the agent during ingest |
| `dataset/task-{train,eval}.jsonl`, `dataset/qa-{train,eval}.jsonl` | generated, committed |
| `dataset/train.py` / `train.ipynb` | Unsloth LoRA + GGUF export |
| `dataset/examples/example-samples.jsonl` | hand-made samples to test the pipeline pre-ingest |
| `dataset/README.md` | full runbook (qa-raw format, RunPod steps, Ollama import, extensions) |
| `.knowledge/` | pi-knowledge binary index (gitignored) |
| `dataset/embeddings/` | exported chunk JSONL snapshots (regenerable via `knowledge_export`; gitignored) |

## 8. Current state (2026-08-18)

- Wiki scaffolding exists (`wiki/` structure, `.base` views); **zero concept pages yet**.
- 24 sources in `raw/` (UU No 6/2023 ×3, PMK, PP, SE, article folders) — none ingested.
- Dataset machinery built and tested: builder runs, generators produce valid
  ShareGPT JSON, split is deterministic. Dataset files are empty by design until
  ingests happen.
- pi-knowledge still global; `.knowledge/` relocation + `pi install -l` not yet applied.

## 9. Next steps (ordered)

1. **Start ingesting** the 24 sources with the strong model (glm-5.1) — this
   bootstraps the wiki *and* the training data simultaneously (steps 11–12 of
   AGENTS.md now run per ingest).
2. Relocate pi-knowledge: create `launch-pi.ps1` (sets `PI_KNOWLEDGE_DIR`),
   `pi install -l npm:pi-knowledge`, index `raw/` + `wiki/`, export JSONL snapshot.
3. At ~30 ingested sources: first training run on RunPod → GGUF → Ollama.
4. v2 (later): `excerpt-raw/` convention for excerpt-level samples from long laws;
   system-prompt variants in the builder.

## 10. Rules & caveats

- Never modify `raw/`.
- Never commit `.knowledge/`, GGUF files, or downloaded model weights.
- Always commit `dataset/*.jsonl` (generated) and `dataset/qa-raw/`.
- Do not train longer than 1–2 epochs, regardless of dataset size.
- Do not expect fine-tuning to store tax-law facts — retrieval is the memory,
  the small model is the reader/writer.
- When in doubt about design intent, read this document before changing
  architecture; extend it after any architecture decision.
