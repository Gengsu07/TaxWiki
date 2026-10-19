# Terms of Use

**Effective date:** 19 October 2026

These terms govern use of the TaxWiki repository — the wiki, sources, tools, dataset, skills, and any model trained from it. By cloning, running, contributing to, or querying TaxWiki, you agree to them.

The software license is [Apache License 2.0](LICENSE). These terms add rules of use. If they conflict with the Apache License on a pure copyright question, the Apache License wins. On privacy and taxpayer data, **these terms win**.

## 1. What TaxWiki is — and is not

TaxWiki is a **personal knowledge base of Indonesian tax concepts, methods, and use cases**. It helps you learn, structure, and retrieve rules (UU, PP, PMK, SE, and related material) and work through **illustrative** examples.

TaxWiki is **not**:

- a substitute for the official statute, regulation, or a current DJP/PMK publication
- tax advice, legal advice, or an opinion you can rely on for a filing, ruling, or dispute
- a system of record for a wajib pajak, a client, or an examination file
- a product that files, calculates a legally binding amount, or represents you before the tax authority

**You must verify every figure, tarif, threshold, and citation against the official source before you use it.** Wiki pages can be draft, stale, or wrong. AI answers can be wrong even when they look cited.

## 2. Do not use real taxpayer data

**This is the primary condition of use. Read it before you add a file or ask a question.**

**You must not input, store, commit, index, embed, train on, or share real taxpayer data in this project.**

Use **concepts, methods, and use cases** only:

- Good: “How does ekualisasi omzet SPT PPh Badan against DPP PPN work, and what breaks it?”
- Good: a worked example with a fictional PT, a placeholder NPWP, and made-up numbers, labeled as ilustrasi.
- Not allowed: a real SPT, faktur, laporan keuangan, NPWP, NIK, nama, alamat, rekening, or case file of an identifiable wajib pajak — even if you “only” paste it into chat so the agent can analyze it.

“Anonymized” is not a shortcut. Removing the name but leaving a unique fact pattern, a real NPWP fragment, or documents that can be re-identified still counts as real taxpayer data. When in doubt, do not add it. Rewrite the question as a method question.

This rule exists because:

- chat with a cloud model leaves your machine
- `raw/`, `wiki/`, and `dataset/` are designed to be committed and reused
- ingest turns sources into training data, so a secret in a source can become a weight in a model

See [PRIVACY.md](PRIVACY.md). Breaking this section is a breach of these terms, whether or not you meant to.

## 3. Acceptable use

You may use TaxWiki to:

- study Indonesian tax rules and the methods for applying them
- ingest **public** legal sources (UU, PP, PMK, PER, SE, public articles) that you have the right to store
- ask conceptual questions and build fictional use cases
- run the local search index and, if you choose, fine-tune a small model on data that complies with section 2

You may not use TaxWiki to:

- hold, process, or circulate real wajib pajak secrets or personal data
- produce a filing, advice, or work product for a real taxpayer and present the model’s answer as checked
- misrepresent wiki text or model output as an official DJP position
- strip copyright notices or present third-party source text as your own beyond what the source’s license and fair dealing allow
- use the tools to attack, scrape, or disrupt systems you are not allowed to access

## 4. No professional reliance

Outputs are educational. They are not a pendapat, advice letter, or pemeriksaan conclusion.

You are solely responsible for:

- checking the law that actually applies to a period and a taxpayer
- any decision, filing, assessment, or advice you make after using this repo
- compliance with kerahasiaan wajib pajak, UU PDP, your office’s rules, and your professional duties

To the maximum extent the law allows, the authors and contributors are not liable for loss, penalty, or missed tax arising from use of or reliance on TaxWiki, including errors in pages, citations, calculations, or model answers.

## 5. Your content

You keep ownership of material you add. You are responsible for having the right to add it.

Do not add to `raw/` or `wiki/`:

- confidential client or employer material
- personal data you have no lawful basis to process
- content you do not have the right to store or to let an AI agent read

Public regulations may be stored for reference. That does not make a copy of a commercial commentary free to redistribute. Respect the source.

If you contribute to this repository, you license your contribution under the Apache License 2.0, and you confirm it contains **no real taxpayer data**.

## 6. AI agents and third parties

Agents that maintain this wiki read files and may send text to a model provider. You choose the agent and the model. Their terms and privacy policies apply to what you send them. TaxWiki does not control those providers and does not promise that a cloud model forgets a prompt.

Local indexing (`.knowledge/`) and local inference (Ollama or similar) stay on your machine only if you configure them that way. A fine-tune job on RunPod, Colab, or any other host is a transfer you initiate — do not upload a dataset that fails section 2.

## 7. No warranty

The wiki, tools, and dataset are provided **“AS IS”**, without warranty of accuracy, completeness, fitness for a particular filing, or non-infringement, except where the Apache License 2.0 states otherwise and the law does not allow a disclaimer.

Tax rules change. A page dated last year can be wrong today. `status: draft` means do not treat it as settled.

## 8. Suspension of the bargain

If you submit real taxpayer data, the permitted use in these terms stops for that material. Remove it. Do not wait to be asked. The authors may decline to ingest, host, or train on any material that looks like real taxpayer data or other confidential content.

## 9. Changes

These terms may be updated in the repository. Continued use after the effective date of a change means you accept the change. The date at the top is the current version.

## 10. Contact

This is a personal project. Questions about these terms go to the repository owner through the project’s normal channel (the git host listed in this repo). Do not send taxpayer data with that question.
