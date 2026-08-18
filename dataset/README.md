# Dataset — fine-tuning pipeline for the TaxWiki agent model

The wiki **accumulates its own training data**. Every ingest with a strong model
(glm-5.1 or similar) produces gold pairs for free:

```
raw/<source>.md  →  wiki/concept/<chapter>/<page>.md   (page-write samples)
wiki page        →  its **Summary** line               (summarize samples)
title + summary  →  chapter                            (classify samples)
```

Because sources are added **incrementally**, the dataset grows incrementally too.
Re-run the builder after every ingest batch — sample identity and the train/eval
split are deterministic (hashed per source), so re-runs only append and git diffs
stay minimal.

## Folder layout

| Path | Purpose | Committed? |
|------|---------|------------|
| `tools/make-dataset.py` | Mines `raw/` + `wiki/` → ShareGPT JSONL | ✅ |
| `dataset/task-{train,eval}.jsonl` | Authoring task samples (generated) | ✅ |
| `dataset/qa-raw/*.jsonl` | Q&A pairs written by the agent during ingest | ✅ |
| `dataset/qa-{train,eval}.jsonl` | Merged QA samples (generated) | ✅ |
| `dataset/manifest.json` | Run summary + accounting (generated) | ✅ |
| `dataset/train.py` | Unsloth LoRA training + GGUF export (RunPod/Colab) | ✅ |
| `dataset/train.ipynb` | Thin Colab wrapper around `train.py` | ✅ |
| `dataset/examples/` | Hand-made samples to test the pipeline before any ingest | ✅ |
| `dataset/models/`, `dataset/*.gguf` | Downloaded fine-tuned weights | ❌ gitignored |

## The accumulate loop

1. **Ingest a source** with the strong model (normal wiki workflow).
2. During ingest, the agent also writes **5–10 Q&A pairs** for each new/updated page
   to `dataset/qa-raw/<source-slug>.jsonl` (see format below). This is what makes
   the fine-tuned model rely on retrieved context instead of hallucinating law text.
3. When pages reach `status: stable` (or `review`), run:

   ```bash
   python tools/make-dataset.py
   ```

4. Commit the JSONL. That's it — data accumulates with zero manual labeling.

## Quality gate

Only pages with `status: stable` or `review` are mined (default). Draft pages are
excluded — they would teach the model your format errors. **The lint pass is also
data cleaning**: fix or exclude any page before it reaches `stable`.

Use `--include-drafts` only for experiments:

```bash
python tools/make-dataset.py --include-drafts
```

## qa-raw format (written by the agent during ingest)

One ShareGPT record per line, per file `dataset/qa-raw/<source-slug>.jsonl`:

```json
{"conversations":[
  {"from":"system","value":"Kamu adalah asisten Wiki Pajak Indonesia. Jawab pertanyaan HANYA berdasarkan konteks yang diberikan. Kutip sumber dengan format (source: nama-file.md). ..."},
  {"from":"human","value":"Konteks:\n<isi halaman wiki>\n\nPertanyaan: <pertanyaan>"},
  {"from":"gpt","value":"<jawaban dengan kutipan>"}
]}
```

## When to train

Not on a schedule — on a data trigger. Train when the dataset meaningfully grew:

- First run: after **~30 ingested sources** (~200–400 task samples), or earlier to
  validate the pipeline using `dataset/examples/` as fallback input.
- After that: when a new major topic was ingested (+100–200 samples) or format
  drift on the small model becomes annoying.

Before training, prefer cheaper levers: zero-shot, few-shot examples in
`AGENTS.md`, or an existing Indonesian model (e.g. SahabatAI). Fine-tuning is the
last lever for style/format locking.

## Training (RunPod / Colab, GPU required)

Unsloth needs an NVIDIA GPU — the 8GB laptop cannot train. Use a spot instance:

```bash
# RunPod: "RunPod Unsloth" template, or any PyTorch CUDA 12.1+ template.
pip install unsloth
pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cu121

git clone <your-repo>
cd <your-repo>
python dataset/train.py --export-gguf
```

| GPU | RAM | Expected time | Spot cost |
|-----|-----|---------------|-----------|
| T4 16GB | 16GB | ~1–2 h | ~$0.20/h |
| L4 / A10 / 4090 24GB | 24GB | ~30–60 min | ~$0.40/h |

Defaults: `unsloth/Phi-4-mini-instruct`, 4-bit, LoRA r=16, **1 epoch**, lr 2e-4,
max_seq_length 4096. Do not train "several hours" — with hundreds of samples that
is overfitting, not quality. One epoch, watch the loss, stop.

Alternatives: `--model unsloth/gemma-3-4b-it`, `--model unsloth/Qwen2.5-3B-Instruct-bnb-4bit`.

## Deploy on the laptop (8GB RAM, no GPU)

Download `outputs/gguf/*-q4_k_m.gguf` (~2.7GB), then:

```bash
ollama create taxwiki-mini -f Modelfile
ollama run taxwiki-mini
```

`Modelfile`:

```
FROM ./taxwiki-mini-q4_k_m.gguf
SYSTEM "Kamu adalah AI pemelihara Wiki Pajak Indonesia ..."
PARAMETER num_ctx 4096
```

Point pi at it as a custom provider (see pi docs: `models.md`, `custom-provider.md`).

## Extension points

`tools/make-dataset.py` has one generator per task type — add more subtasks
(log-entry writing, learning-path node writing) as new functions following
`gen_page_write` and register them in `main()`. Keep the rule: **one sample = one
scoped subtask**, never the full 15-file ingest cascade.
