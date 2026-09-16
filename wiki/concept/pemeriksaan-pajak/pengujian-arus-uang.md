---
title: Pengujian Arus Uang
tags: [concept, pemeriksaan-pajak]
date: 2026-08-26
sources: [se65_pj_2013_metode_teknik_pemeriksaan.md]
aliases: [Arus Uang, Cash Flow Test, Pengujian Kas dan Bank]
status: stable
chapter: pemeriksaan-pajak
difficulty: beginner
estimated_minutes: 15
---
# Pengujian Arus Uang

**Summary**: Teknik pemeriksaan yang mencakup transaksi kas, bank, dan setara kas untuk menguji aliran uang suatu transaksi dan/atau mendapatkan jumlah penerimaan uang dalam suatu kurun waktu — mendukung pengujian kebenaran penghasilan bruto yang dilaporkan Wajib Pajak secara **kas (cash basis)** (source: se65_pj_2013_metode_teknik_pemeriksaan.md).

---

## Tujuan

Pengujian arus uang dilakukan untuk menguji aliran uang suatu transaksi dan mendapatkan jumlah penerimaan uang dalam suatu kurun waktu, dalam rangka mendukung pengujian kebenaran penghasilan bruto yang dilaporkan Wajib Pajak berdasarkan **kas (cash basis)**. Cakupannya meliputi **kas, bank, dan setara kas lainnya** (source: se65_pj_2013_metode_teknik_pemeriksaan.md).

Ini adalah teknik pertama dari tiga teknik pengujian keterkaitan, bersama [[pengujian-arus-piutang]] dan [[pengujian-arus-utang]].

## Formula

```
Saldo Akhir Kas/Bank           +/+
Pengeluaran Kas/Bank           +/+
Saldo Awal Kas/Bank            -/-
Penyesuaian non penghasilan    +/-
-----------------------------------
Penerimaan Kas/Bank            xxx
```

(source: se65_pj_2013_metode_teknik_pemeriksaan.md)

**Logika**: kenaikan saldo kas/bank selama satu tahun pajak (saldo akhir − saldo awal) berasal dari penerimaan dikurangi pengeluaran; sehingga penerimaan = (saldo akhir − saldo awal) + pengeluaran.

**Cara alternatif**: pengujian juga dapat dilakukan dengan menghitung langsung **sisi penerimaan saja** (menjumlahkan seluruh penerimaan dari buku kas/bank), tanpa melalui saldo dan pengeluaran (source: se65_pj_2013_metode_teknik_pemeriksaan.md).

## Penyesuaian non penghasilan

Penerimaan kas/bank yang diperoleh dari formula **harus mengeluarkan penerimaan yang tidak ada kaitannya dengan penghasilan**, yang dikelompokkan sebagai penyesuaian non penghasilan, antara lain (source: se65_pj_2013_metode_teknik_pemeriksaan.md):

- **transfer antar bank** (bukan penghasilan, hanya perpindahan uang);
- **penerimaan pinjaman** (pencairan pinjaman bank/afiliasi/pemegang saham);
- **PPN dipungut sendiri** (titipan PPN dari pelanggan);
- setoran modal dan penerimaan lain yang bukan penghasilan;
- serta memperhitungkan **saldo uang muka penjualan/pelanggan** jika ada.

### Perhatian khusus: PPN dipungut sendiri

Nilai PPN dipungut sendiri yang dikeluarkan dari penerimaan dapat diperoleh dari (source: se65_pj_2013_metode_teknik_pemeriksaan.md):

1. nilai yang dilaporkan pada **SPT Masa PPN**;
2. **penelusuran jurnal** setiap transaksi PPN; atau
3. **mutasi utang PPN** pada buku besar.

Apabila menggunakan angka dari SPT Masa PPN, pastikan jumlah itu **tidak termasuk PPN yang dilaporkan tetapi tidak terdapat aliran uang masuk ke kas/bank**, yaitu:

- PPN yang **ditanggung sendiri** oleh Wajib Pajak (pemberian cuma-cuma, pemakaian sendiri, sampel, dll);
- PPN yang **dipungut beda waktu** (faktur telah diterbitkan tetapi pelunasan belum diterima, atau sebaliknya);
- transaksi lain yang nyata-nyata tidak terdapat titipan PPN dalam penerimaan uang yang dihitung.

## Langkah praktis menyusun arus uang

1. Ambil **mutasi buku kas dan buku bank** selama tahun pajak: saldo awal, seluruh penerimaan, seluruh pengeluaran, saldo akhir.
2. Pastikan kebenaran saldo dan mutasi (rekonsiliasi dengan rekening koran).
3. Saring **penyesuaian non penghasilan** (transfer antar bank, pinjaman, PPN dipungut sendiri, setoran modal).
4. Perhitungkan **uang muka penjualan/pelanggan** jika ada.
5. Hasil = **penerimaan kas/bank dari penghasilan** → dibandingkan dengan penjualan tunai / penghasilan bruto menurut SPT.

## Contoh perhitungan

| Pos | Nilai |
|---|---:|
| Saldo awal kas/bank | 200 |
| Saldo akhir kas/bank | 350 |
| Pengeluaran kas/bank setahun | 1.000 |
| **Penerimaan bruto** = 350 + 1.000 − 200 | **1.150** |
| (−) Transfer antar bank | (100) |
| (−) Pencairan pinjaman | (200) |
| (−) PPN dipungut sendiri dalam penerimaan | (50) |
| **Penerimaan dari penghasilan** | **800** |

Angka 800 dibandingkan dengan penjualan tunai menurut SPT — selisih berindikasi penjualan tunai yang tidak dilaporkan (contoh ilustratif).

## Posisi dalam pengujian keterkaitan

| Teknik | Digunakan untuk mendapatkan |
|--------|-----------------------------|
| **Pengujian arus uang** | Nilai **tunai** dari penjualan dan penghasilan bruto |
| [[pengujian-arus-piutang\|Pengujian arus piutang]] | Nilai pelunasan **non-tunai** |
| [[pengujian-arus-utang\|Pengujian arus utang]] | Uang muka penjualan/pelanggan atau penghasilan bruto secara **akrual** |

Ketiganya dapat digabung menjadi pengujian atas **arus uang dan utang-piutang** untuk mendapatkan nilai tunai dan akrual penghasilan bruto sekaligus — lihat grid pos 1a–7 pada [[pengujian-arus-piutang]] (source: se65_pj_2013_metode_teknik_pemeriksaan.md).

## Related pages

- [[pengujian-arus-piutang]]
- [[pengujian-arus-utang]]
- [[concept/pemeriksaan-pajak/_learning-path|Learning Path: Pemeriksaan Pajak]]
- [[_learning-path|Master Learning Path]]
