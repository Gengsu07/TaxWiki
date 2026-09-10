---
title: Operations Log
tags: [meta, log]
date: 2026-05-24
status: stable
---

# Operations Log

> **TL;DR**: An append-only chronological record of every operation performed on the wiki — source ingestions, concept page creations, learning path updates, and structural changes. Each entry records the date, the source or trigger, and a summary of what changed. This log is the wiki's audit trail [1].

---

## Format

Every log entry follows this structure:

```
### YYYY-MM-DD — [Operation Type]: [Short Description]

**Source/Trigger**: [What prompted this — a raw file, user request, or lint pass]
**Pages created**: [List of new pages]
**Pages updated**: [List of modified pages]
**Learning paths updated**: [List of _learning-path.md files changed]
**Summary**: [1–3 sentences describing the net effect]
```

---

### 2026-08-24 — [Infra]: Knowledge base launcher scripts

**Source/Trigger**: User request — create `launch-pi.ps1` and `launch-pi.sh` so pi sessions attach to the project KB in `.knowledge/`
**Pages created**: None
**Pages updated**: None
**Learning paths updated**: None
**Summary**: Added `launch-pi.ps1` (PowerShell) and `launch-pi.sh` (bash, executable) which set `PI_KNOWLEDGE_DIR` to the repo's `.knowledge/` before launching pi, per TAXWIKIDESIGN.md §6. Verified the `.sh` variant launches pi 0.82.1 with the env var set. The existing "Indonesian Tax Wiki" KB (158 chunks from `raw/`) was previously unreachable because sessions defaulted to the global knowledge dir.

### 2026-08-24 — [Infra]: KB extended with wiki pages + JSONL snapshots

**Source/Trigger**: Follow-up to launcher scripts — index `wiki/` and export portable snapshots from an attached headless pi run
**Pages created**: None
**Pages updated**: None
**Learning paths updated**: None
**Summary**: Added KB "TaxWiki Wiki Pages" (162 chunks from 10 `wiki/` files, 100% coverage). Verified "Indonesian Tax Wiki" covers all 24 real `raw/` files (only the `assets/.gitkeep` placeholder is excluded; the PKP PDF is included). Exported portable snapshots `wiki/embeddings/indonesian-tax-wiki.jsonl` (158 chunks) and `wiki/embeddings/taxwiki-wiki-pages.jsonl` (162 chunks) per TAXWIKIDESIGN.md §6; `.knowledge/` stays gitignored and is rebuildable via `knowledge_import`.

### 2026-08-24 — [Ingest]: Concept page pertama — Pengujian Arus Piutang (SE-65/PJ/2013)

**Source/Trigger**: User request — buat halaman konsep "Pengujian Arus Piutang" dari sumber `raw/se65_pj_2013_metode_teknik_pemeriksaan.md` (bagian "Pengujian Arus Piutang")
**Pages created**: `wiki/concept/pemeriksaan-pajak/pengujian-arus-piutang.md` (concept, stable), `wiki/concept/pemeriksaan-pajak/_learning-path.md` (chapter path baru, 1 node)
**Pages updated**: `wiki/index.md` (tabel chapter + mermaid master path), `wiki/_learning-path.md` (node baru "Pemeriksaan Pajak" posisi 2; Cross-Cutting bergeser ke 3)
**Learning paths updated**: `wiki/concept/pemeriksaan-pajak/_learning-path.md` (baru), `wiki/_learning-path.md` (master)
**Summary**: Chapter pertama topik `pemeriksaan-pajak` dibuat dengan konsep pengujian arus piutang: tujuan, dua cara pengujian, 6 penyesuaian, formula peredaran usaha, grid pengujian gabungan arus uang + utang piutang, dan peran tiap teknik. Q&A pairs (8) ditulis ke `dataset/qa-raw/se65_pj_2013_metode_teknik_pemeriksaan.jsonl`; `tools/make-dataset.py` dijalankan.

### 2026-08-24 — [Infra]: Token-bloat optimization (KB feedback loop + Q&A guardrails)

**Trigger**: User noticed input token usage exploding when asking questions.
**Root cause**: `wiki/embeddings/*.jsonl` (KB export snapshots) lived inside `wiki/`, and the "TaxWiki Wiki Pages" KB indexes the whole `wiki/` dir — so 321 of 347 chunks (92%, ~1.9 MB) were the KB re-indexing its own export as quoted JSON (~6000 chars ≈ 1500-2000 tokens per junk chunk). Secondary causes: raw UU docs (120-244 KB each) read in full during Q&A ≈ 30-60k tokens per read.
**Changes**:
- Moved export snapshots `wiki/embeddings/*.jsonl` → `dataset/embeddings/` (gitignored; regenerable via `knowledge_export`); deleted empty `wiki/embeddings/`
- Updated `.pi/build-knowledge.mjs` export path + warning comment
- `knowledge_update` "TaxWiki Wiki Pages": 347 → 43 chunks (−323 junk); "Indonesian Tax Wiki": 158 chunks unchanged
- `AGENTS.md` Q&A workflow rewritten: search KBs first (`mode: hybrid`, `limit: 4-6`), never read `raw/` files during Q&A
- `TAXWIKIDESIGN.md` export convention updated; `.gitignore` covers `dataset/embeddings/`
**Result**: wiki KB shrank 88% (1.9 MB → 40 KB of real content); per-question search output no longer contains duplicated/escaped JSON chunks.

### 2026-08-24 — [Concept]: Objek PPh 21 terkait BPJS — bab baru Pajak Penghasilan

**Source/Trigger**: User request — simpan jawaban Q&A "objek PPh 21 terkait BPJS" sebagai halaman konsep
**Pages created**: `wiki/concept/pajak-penghasilan/pph-21-bpjs.md` (concept, stable), `wiki/concept/pajak-penghasilan/_learning-path.md` (chapter path baru, 1 node)
**Pages updated**: `wiki/_learning-path.md` (node baru "Pajak Penghasilan" posisi 3; Cross-Cutting bergeser ke 4), `wiki/index.md` (mermaid master path + tabel chapter)
**Learning paths updated**: `wiki/concept/pajak-penghasilan/_learning-path.md` (baru), `wiki/_learning-path.md` (master)
**Summary**: Chapter baru `pajak-penghasilan` dibuat dengan konsep PPh 21 dan BPJS: prinsip objek = iuran yang dibayar pemberi kerja (JKK/JKM masuk penghasilan bruto per PMK 168/2023 Pasal 5 ayat (3) huruf d; umum Pasal 9 ayat (1) huruf d UU PPh), bagian bukan objek (iuran porsi pegawai, manfaat yang diterima tidak dipajaki lagi), pengurang penghasilan bruto (iuran pensiun termasuk THT, Pasal 21 ayat (3)), dan tarif iuran JHT 5,7% (3,7%+2%) serta JP 3% (2%+1%). Belum menulis Q&A pairs ke dataset (offering ke user).

### 2026-08-26 — [Concept]: KLU 47301 — Proses Bisnis Perdagangan Eceran Bahan Bakar di SPBU — bab baru Proses Bisnis (probis)

**Trigger**: User request — jelaskan & simpan proses bisnis "perdagangan eceran bahan bakar di sarana pengisian bahan bakar" (KLU 47301) dengan unsur perpajakan detail + ilustrasi mermaid berlabel jenis pajak
**Pages created**: `wiki/concept/probis/47301-perdagangan-eceran-bahan-bakar-di-sarana-pengisian-bahan-bakar.md` (concept, stable), `wiki/concept/probis/_learning-path.md` (chapter path baru, 1 node)
**Pages updated**: `wiki/_learning-path.md` (node baru "Proses Bisnis (KLU)" posisi 4; Cross-Cutting bergeser ke 5), `wiki/index.md` (mermaid master path + tabel chapter)
**Learning paths updated**: `wiki/concept/probis/_learning-path.md` (baru), `wiki/_learning-path.md` (master)
**Q&A pairs**: `dataset/qa-raw/47301-perdagangan-eceran-bahan-bakar.jsonl` (7 pasang) → `tools/make-dataset.py` dijalankan
**Summary**: Bab baru `probis/` dibuat dengan konsep KLU 47301: rantai produsen/importir → badan usaha niaga → penyalur/agen (SPBU) → konsumen akhir; PPh 22 dipungut produsen/importir saat terbit Delivery Order (0,25% SPBU-Pertamina, 0,3% lainnya; FINAL bagi penyalur/agen, TIDAK FINAL bagi selain penyalur/agen — pembeda = status izin penyaluran, bukan bentuk badan); PPN dikenakan di setiap penyerahan, efektif 11% (12% × 11/12 DPP, PMK 131/2024 jo PMK 11/2025), Faktur Pajak Digunggung di eceran, tidak ada konsep "PPN final"; PBBKB pajak daerah (UU 1/2022); PPh normal atas marjin SPBU. Sumber utama: PMK 51/2025 (menggantikan PMK 34/2017 jo 41/2022 per 25 Juli 2025), Permen ESDM 13/2018, KBLI 2020, riset web DDTC/Pajakku/BNK. Perlu verifikasi lanjut: PPN BBM bersubsidi & tarif PBBKB per daerah.

### 2026-09-10 — [Sync]: PPh 21 dan BPJS — lengkapi fakta dari `Subjek Pilihan - PPh Pasal 2126.md`

**Source/Trigger**: User request — sinkronkan `wiki/concept/pajak-penghasilan/pph-21-bpjs.md` dengan sumber `raw/PPh 21/Subjek Pilihan - PPh Pasal 2126.md` (sumber sudah ada di `sources` frontmatter, tetapi isinya belum sepenuhnya tercermin)
**Pages created**: None
**Pages updated**: `wiki/concept/pajak-penghasilan/pph-21-bpjs.md` (sync, status tetap `stable`)
**Learning paths updated**: None
**Summary**: Fakta-fakta dari sumber yang sebelumnya hilang ditambahkan: (1) tarif JKK 5 kelompok risiko per PP 44/2015 Pasal 16 (0,24% / 0,54% / 0,89% / 1,27% / 1,74%); (2) tarif JKM 0,30% per PP 44/2015 Pasal 18; (3) **fakta besar yang sebelumnya hilang: iuran JHT dan JP yang dibayar pemberi kerja adalah PENGURANG PPh 21, diterapkan pada masa pajak terakhir (Desember atau bulan berhenti kerja)**; (4) sitasi Pasal 7 huruf c PMK 168/2023 untuk pengecualian JHT/JP pemberi kerja dari objek; (5) sitasi Pasal 7 huruf a PMK 168/2023 untuk pengecualian manfaat/santunan. Tabel ringkasan diperluas dari 5 baris menjadi 8 baris untuk membedakan secara eksplisit porsi pemberi kerja vs porsi pegawai untuk JHT dan JP. Karena ini sync (bukan ingest sumber baru), `wiki/concept/pajak-penghasilan/_learning-path.md` dan master path tidak diupdate.

### 2026-08-26 — [Concept]: Pengujian Arus Uang & Pengujian Arus Utang — tambahan bab Pemeriksaan Pajak

**Trigger**: User request — simpan jawaban Q&A "bagaimana membuat arus utang untuk menguji pembelian" dan "bagaimana membuat arus uang" sebagai halaman konsep (sumber yang sama: SE-65/PJ/2013, bukan ingest baru)
**Pages created**: `wiki/concept/pemeriksaan-pajak/pengujian-arus-uang.md` (concept, stable), `wiki/concept/pemeriksaan-pajak/pengujian-arus-utang.md` (concept, stable)
**Pages updated**: `wiki/index.md` (tabel chapter: node pemeriksaan-pajak 1 → 3), `wiki/concept/pemeriksaan-pajak/_learning-path.md` (urutan ulang: 1 arus uang → 2 arus piutang → 3 arus utang; mermaid + overview + prerequisites)
**Summary**: Dua halaman konsep baru melengkapi teknik pengujian keterkaitan dari SE-65/PJ/2013: (1) Pengujian Arus Uang — formula penerimaan kas/bank (saldo akhir + pengeluaran − saldo awal), cara alternatif sisi penerimaan, penyesuaian non penghasilan (transfer antar bank, pinjaman, PPN dipungut sendiri, uang muka pelanggan), dan penanganan PPN dipungut sendiri dari SPT Masa PPN/jurnal/mutasi utang PPN; (2) Pengujian Arus Utang — pemilihan akun utang sesuai pos yang diuji, formula pembelian (saldo akhir utang usaha + pembelian tunai + pelunasan − saldo awal), formula uang muka penjualan/pelanggan, penyesuaian mutasi utang non-pembelian, dan contoh perhitungan. Belum menulis Q&A pairs ke dataset (offering ke user).

### 2026-09-10 — [Concept]: PPh 23 atas Jasa — tambahan node 2 bab Pajak Penghasilan

**Source/Trigger**: User request — simpan jawaban Q&A "pengenaan PPh Pasal 23 untuk jasa telekomunikasi Telkom Astinet (internet); apakah Telkom dikecualikan dan memiliki SKB" sebagai halaman konsep, fokus pada aturan jasa yang merupakan objek PPh 23. Riset web: PMK 141/2015 (proscg/JDIH/klikpajak), S-813/PJ.032/2007 (aguspajak), SE-30/PJ.43/2001 (ddtc), pajak.go.id (Pemotongan PPh 23, SKB), nusa.net KB.
**Pages created**: `wiki/concept/pajak-penghasilan/pph-23-jasa.md` (concept, stable)
**Pages updated**: `wiki/index.md` (tabel chapter: node pajak-penghasilan 1 → 2)
**Learning paths updated**: `wiki/concept/pajak-penghasilan/_learning-path.md` (node 2 "PPh 23 atas Jasa" — mermaid A→B + overview + prerequisites)
**Q&A pairs**: `dataset/qa-raw/pph-23-jasa.jsonl` (8 pasang) → `tools/make-dataset.py` dijalankan
**Summary**: Halaman konsep PPh 23 atas jasa: (1) prinsip positive list — hanya 62 jenis jasa di Lampiran PMK 141/PMK.03/2015 yang objek, tarif 2% dari jumlah bruto tidak termasuk PPN (tanpa NPWP 4%), KJS 104, setor tgl 10/lapor tgl 20, e-Bupot; (2) pengecualian umum: jasa tak tercantum (jasa telekomunikasi umum/telepon per S-813/PJ.032/2007), penghasilan ber-PPh final (Pasal 1(2) PMK 141: sewa tanah/bangunan PPh 4(2), jasa konstruksi PP 9/2022), pengecualian Pasal 23(4) UU PPh (bank, financial lease, dividen ≥25%, bagian laba, SHU koperasi, bunga penyalur pinjaman), jasa ranah PPh 21; (3) SKB: bukan objek tak perlu SKB; objek hanya SKB yang meniadakan pemotongan; kriteria SKB umumnya WP UMKM PP 23/2018 (Surat Keterangan PP 23/2018) dan WP OP di bawah PTKP; (4) studi kasus Astinet: "jasa internet termasuk sambungannya" = butir 23 PMK 141 → objek 2%; Telkom tidak dikecualikan dan tidak punya SKB; telepon bukan objek; interkoneksi historis objek (SE-30) tetapi tak lagi di daftar PMK 141.
