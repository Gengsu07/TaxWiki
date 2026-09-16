---
title: Ekualisasi PPh Badan dan PPN
tags: [concept, pemeriksaan-pajak]
date: 2026-09-15
sources: [se65_pj_2013_metode_teknik_pemeriksaan.md]
aliases: [Ekualisasi, Rekonsiliasi PPh PPN, Ekualisasi Omset, Ekualisasi Pembelian]
status: draft
chapter: pemeriksaan-pajak
difficulty: intermediate
estimated_minutes: 25
---
# Ekualisasi PPh Badan dan PPN

**Summary**: Proses memastikan konsistensi angka antara SPT Tahunan PPh Badan (1771) dan SPT Masa PPN (1111) dalam satu tahun pajak, di dua sisi: **omset/peredaran usaha** (penjualan) dan **pembelian/beban**. Selisih yang tidak dapat dijelaskan menjadi indikasi penghasilan tidak dilaporkan, Pajak Masukan fiktif, atau pemotongan PPh 23/22 yang kurang.

> **Status**: halaman ini `draft` — bagian "langkah & penyebab selisih" adalah praktik umum yang belum diverifikasi ke sumber resmi. Bagian yang bersumber dari [[pengujian-arus-uang]], [[pengujian-arus-piutang]], dan [[pengujian-arus-utang]] (SE-65/PJ/2013) sudah terverifikasi.

---

## Konsep dasar

PPh Badan dihitung dari **penghasilan neto fiskal** (basis akrual), sedangkan PPN dipungut atas **penyerahan barang/jasa kena pajak** (basis terutang saat penyerahan/pembayaran yang lebih dulu). Keduanya tidak selalu sama angkanya, tetapi harus **konsisten dan dapat dijelaskan selisihnya**. Ekualisasi dilakukan dua arah:

1. **Sisi omset**: penjualan/peredaran usaha di 1771 vs total DPP penyerahan di seluruh SPT Masa PPN.
2. **Sisi pembelian**: pembelian/beban di 1771 (HPP, biaya, capex) vs DPP Pajak Masukan yang dikreditkan di SPT Masa PPN.

## Ekualisasi omset

**Data**: SPT Tahunan 1771 (lampiran laba rugi), 12 SPT Masa PPN 1111, buku besar penjualan, daftar faktur pajak keluaran, rekening koran.

**Langkah**:

1. Hitung **peredaran usaha fiskal**: penjualan neto laba rugi ± koreksi fiskal atas penjualan.
2. Hitung **omzet PPN**: total DPP penyerahan di SPT Masa PPN (terutang + tidak terutang + ekspor).
3. Bandingkan → **selisih awal**.
4. Jelaskan selisih dengan pos-pos analisis berikut (per masa, lalu total tahunan).

| Penyebab selisih omset | Pengaruh |
|---|---|
| Penghasilan bukan penjualan (bunga, jasa giro, dividen, laba selisih kurs) | Ada di PPh, tidak kena PPN |
| Penjualan kena PPh final (sewa tanah/bangunan, jasa konstruksi, pengalihan tanah/bangunan) | Masuk PPh final; PPN terutang/bebas bisa berbeda |
| Ekspor | PPN 0% tetap dilaporkan di SPT Masa PPN; masuk peredaran usaha PPh |
| DPP nilai lain / faktur digunggung (penjualan eceran) | Angka DPP berbeda dari harga jual |
| Pemakaian sendiri / pemberian cuma-cuma | Kena PPN tapi bukan penjualan di laba rugi |
| Retur, diskon, penyesuaian harga | Mengurangi omzet PPN dan/atau PPh beda waktu |
| Uang muka pelanggan; beda masa terbit faktur | Beda waktu pengakuan |

## Ekualisasi pembelian

**Langkah**:

1. Hitung **total pembelian/beban fiskal**: pembelian barang dagangan & bahan (HPP) + beban jasa & biaya operasional + perolehan aset (capex) ± koreksi fiskal atas beban.
2. Hitung **DPP Pajak Masukan yang dikreditkan** dari seluruh SPT Masa PPN (1111). Kerjakan di angka **DPP**, bukan PPN-nya, karena tarif efektif 12% dengan DPP 11/12 untuk sebagian besar penyerahan.
3. Bandingkan → **selisih**; jelaskan dengan pos berikut. Selisih `> 0` (beban tanpa PM) umum dan wajar; selisih `< 0` (PM dikreditkan tanpa beban) indikasi masalah.

| Penyebab selisih pembelian | Pengaruh |
|---|---|
| Pembelian dari non-PKP / pedagang eceran | Beban PPh ada, PM tidak ada/digunggung |
| PM tidak dapat dikreditkan (Pasal 9 ayat (8) UU PPN/PMK 18/2021: sedan, makanan-minuman, dll) | Beban PPh ada, PM tidak dikreditkan |
| Beban tanpa PPN (gaji, bunga, PPh, denda, asuransi) | Beban PPh, tidak ada PPN |
| Impor | PPN impor via SSP, mekanisme berbeda |
| Uang muka pembelian | Beda waktu terutang |
| Capex (DPP PM penuh) vs penyusutan (beban PPh bertahap) | Beda pengakuan aset |
| PM dikreditkan tanpa pembelian di laba rugi | ⚠️ Indikasi PM fiktif/bermasalah |
| PM belum dikreditkan / tidak dilaporkan (retur, PM kolektif) | Beban PPh ada, PM nol |

**Cross-check PPh 23/22**: pembelian jasa harus disertai pemotongan PPh 23 (2% dari jumlah bruto tidak termasuk PPN — lihat [[pph-23-jasa]]) dan PPN dipungut; pembelian dari pemungut PPh 22 harus ada bukti pungut. Konsistensi ketiganya (PPh, PPN, laporan laba rugi) adalah inti ekualisasi.

## Kaitan dengan teknik pemeriksaan

Ekualisasi adalah sisi kepatuhan dari teknik pengujian keterkaitan yang dipakai Pemeriksa Pajak (SE-65/PJ/2013):

- [[pengujian-arus-uang]] — penerimaan kas/bank; **PPN dipungut sendiri** dikeluarkan dari penerimaan sebagai penyesuaian non penghasilan. Angka PPN dipungut sendiri diambil dari **SPT Masa PPN** (pastikan tidak termasuk PPN tanpa aliran uang masuk kas/bank: ditanggung sendiri, cuma-cuma, pemakaian sendiri, dipungut beda waktu).
- [[pengujian-arus-piutang]] — grid pos 1a–7: penghasilan bruto **termasuk PPN** (pos 3), dikurangi PPN dipungut sendiri (pos 4), menjadi penghasilan bruto menurut Pemeriksa (pos 5) yang dibandingkan dengan SPT WP (pos 6) → selisih (pos 7).
- [[pengujian-arus-utang]] — formula pembelian; "selisih berimplikasi pada PPh 23/22 yang kurang dipotong dan Pajak Masukan yang tidak sah dikreditkan".

Konsistensi yang ditegakkan ekualisasi (omzet & pembelian) adalah premis yang sama persis dengan pengujian keterkaitan: setiap penerimaan terkandung PPN, setiap pemasukan ada faktur, setiap beban ada dasar PM yang sah.

## Working paper

Tersedia berkas Excel yang siap diisi: **[[./working-papers/ekualisasi-pph-ppn.xlsx]]**

- Sheet **Omset** & **Pembelian**: input per masa (Jan–Des), Total dan selisih otomatis (formula), pos analisis selisih, kondisi format (selisih ≠ 0 berubah merah).
- Sheet **Panduan**: cara pakai, aturan tanda penyesuaian, daftar penyebab selisih.
- Generator: `tools/make-ekualisasi-workbook.py` (bisa dijalankan ulang jika ingin mengubah struktur).

## Catatan verifikasi (status draft)

- Tarif PPN 12% dengan DPP 11/12 untuk sebagian besar penyerahan (PMK 131/2024 jo PMK 11/2025) — sudah direfleksikan di [[47301-perdagangan-eceran-bahan-bakar-di-sarana-pengisian-bahan-bakar]] (contoh angka 12% × 11/12).
- Pos penyebab selisih di kedua tabel perlu diverifikasi dengan sumber resmi (SE-65/PJ/2013 sebagai dasar pengujian; ketentuan PM Pasal 9 UU PPN/PMK 18/2021 untuk pengkreditan PM).
- Kategori pengecualian PM yang tidak dapat dikreditkan (Pasal 9 ayat (8)) menunggu konfirmasi cakupan persis tahun pajak berjalan.

## Related pages

- [[pengujian-arus-uang]]
- [[pengujian-arus-piutang]]
- [[pengujian-arus-utang]]
- [[pph-23-jasa]]
- [[concept/pemeriksaan-pajak/_learning-path|Learning Path: Pemeriksaan Pajak]]
- [[_learning-path|Master Learning Path]]