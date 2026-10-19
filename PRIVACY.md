# Privacy Statement

**Effective date:** 19 October 2026

TaxWiki is a personal, local knowledge base for **Indonesian tax concepts, methods, and use cases**. It is not a tax-filing service, not a client file, and not a place to store real taxpayer records.

## The rule, in one sentence

**Do not put real taxpayer data into this project.** Use concepts, methods, and fictional or fully anonymized use cases only.

## What “real taxpayer data” means

Do **not** add, paste, upload, or discuss any of the following in chat, in `raw/`, in `wiki/`, in `working-papers/`, in `dataset/`, or in any other file in this repository:

- Nama wajib pajak, NPWP, NIK, NITKU, nomor paspor, or other identity numbers
- Alamat, nomor telepon, email, rekening bank, or other contact and financial identifiers
- SPT, faktur pajak, bukti potong, laporan keuangan, buku besar, or other filings and books that belong to a real person or entity
- Data pegawai, vendor, pelanggan, or lawan transaksi that can identify a real party
- Case files, pemeriksaan, keberatan, or banding materials tied to a real wajib pajak
- Anything else that, alone or combined, identifies a real taxpayer or their affairs

**Use instead:** fictional names, placeholder NPWP (for example `00.000.000.0-000.000`), rounded illustrative figures, and descriptions of the **method** — how to classify a transaction, how to equalize a return, how a rule applies — without a real subject.

If a source document contains real identities, strip them **before** it enters `raw/`. Once a fact is in the repo it can be committed, indexed, embedded, and turned into training samples. Deleting it later does not reliably erase copies.

## What this project stores

TaxWiki runs on your machine. There is no TaxWiki account and no TaxWiki server that receives your files.

| What | Where | Leaves your machine? |
| --- | --- | --- |
| Source documents you add | `raw/` (committed if you commit them) | Only if you push the git remote or share the folder |
| Wiki pages, logs, Q&A | `wiki/`, `dataset/` | Same — git push or folder share |
| Local search index and model cache | `.knowledge/` (gitignored) | No, unless you copy the folder |
| Chat with your AI agent | Your agent's own history and, if you use a cloud model, that provider | **Yes, if the agent sends prompts to a cloud model** |

Cloud agents (and any cloud model your local agent calls) receive the text you put in the conversation and any files the agent reads. **Treat every prompt as if it will be sent to a third party.** That is another reason real taxpayer data does not belong here.

## What we do not do

- We do not sell data. There is no advertising and no analytics product.
- We do not operate a hosted service, so we do not collect accounts, cookies, or usage telemetry through this repository.
- We do not guarantee that third-party tools you choose to run (Obsidian, git hosts, AI providers, RunPod/Colab, Ollama) follow this statement. Read their policies before you send them anything.

## Fine-tuning

Ingest writes Q&A pairs into `dataset/` and can be used to fine-tune a local model. **Training data is mined from this repository.** If real taxpayer data is in the wiki, it can end up in a model. Do not train on, export, or share a dataset that contains real taxpayer data.

## If something real slipped in

1. Stop. Do not commit, push, ingest, or index it.
2. Remove it from the working tree and from chat.
3. If it was already committed or pushed, treat the git history and any remote, index, and dataset copy as exposed. Rewrite or delete those copies, and rotate or notify as your own obligations require.
4. This project cannot “unsee” data already sent to a cloud model provider. Contact that provider if you need deletion.

## Your responsibility

You are the controller of whatever you put into this vault. Indonesian rules on taxpayer secrecy and personal data (including UU KUP on kerahasiaan wajib pajak and UU Pelindungan Data Pribadi, where they apply to you) are yours to follow. This statement is a project rule, not legal advice, and it does not reduce those duties.

## Changes

This statement may be updated in the repository. The effective date at the top is the version that applies.
