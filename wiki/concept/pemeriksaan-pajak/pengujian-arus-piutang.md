---
title: Pengujian Arus Piutang
tags: [concept, pemeriksaan-pajak]
date: 2026-08-24
sources: [se65_pj_2013_metode_teknik_pemeriksaan.md]
aliases: [Arus Piutang, Receivables Flow, Pengujian Piutang Usaha]
status: stable
chapter: pemeriksaan-pajak
difficulty: intermediate
estimated_minutes: 20
---
# Pengujian Arus Piutang

**Summary**: Teknik pemeriksaan untuk menghitung pelunasan piutang usaha dalam suatu kurun waktu, guna menguji kebenaran penghasilan bruto yang dilaporkan Wajib Pajak secara akrual — dilakukan dengan dua cara: hanya melalui mutasi kredit akun piutang usaha, atau digabungkan dengan pengujian arus uang dan utang-piutang (source: se65_pj_2013_metode_teknik_pemeriksaan.md).

---

## Tujuan

Pengujian arus piutang dilakukan untuk mendapatkan **jumlah pelunasan piutang usaha dalam suatu kurun waktu** dalam rangka mendukung pengujian kebenaran penghasilan bruto yang dilaporkan Wajib Pajak secara **akrual (accrual basis)** (source: se65_pj_2013_metode_teknik_pemeriksaan.md).

Pengujian ini adalah salah satu dari tiga "teknik pengujian keterkaitan" dalam pemeriksaan, bersama [[pengujian-arus-uang-tunai|pengujian arus uang]] dan pengujian arus utang.

## Dua cara pengujian

1. **Cara 1 — hanya mutasi kredit akun piutang usaha.** Digunakan untuk mendapatkan penjualan secara akrual (non tunai). Jika ingin mendapatkan penjualan secara total (tunai dan non tunai), maka hasilnya harus ditambahkan dengan hasil penghitungan penjualan tunai (source: se65_pj_2013_metode_teknik_pemeriksaan.md).
2. **Cara 2 — menggabungkan hasil pengujian arus uang dan utang-piutang sekaligus.** Untuk mendapatkan penghasilan bruto baik dari tunai maupun non tunai. Caranya: menggunakan penerimaan uang/tunai dan non tunai — seperti offset utang-piutang, bukti potong, bukti pungut — sebagai unsur pelunasan piutang usaha, serta memperhatikan saldo-saldo **uang muka pelanggan** ataupun **pendapatan ditangguhkan** (source: se65_pj_2013_metode_teknik_pemeriksaan.md).

## Penyesuaian yang harus diperhitungkan

Saat menyusun arus piutang, pemeriksa wajib memperhitungkan penyesuaian berikut (source: se65_pj_2013_metode_teknik_pemeriksaan.md):

1. **Ditambah** penghapusan piutang (write-off);
2. **Dikurangi** retur penjualan;
3. **Dikurangi** PPN dipungut sendiri yang ada dalam penerimaan kas/bank;
4. Saldo-saldo uang muka penjualan/pelanggan;
5. Saldo-saldo pendapatan yang ditangguhkan;
6. Penyesuaian lain yang tidak ada hubungan dengan penerimaan dan penghasilan.

## Formula arus piutang

```
Pelunasan/Penerimaan melalui Kas/Bank        +/+
Pelunasan Non Kas/Bank                       +/+
Saldo Akhir Piutang Usaha                    +/+
Saldo Awal Piutang Usaha                     -/-
Penyesuaian                                  +/-
-----------------------------------------------
Peredaran Usaha                              xxx
```

(source: se65_pj_2013_metode_teknik_pemeriksaan.md)

## Pengujian gabungan arus uang dan utang piutang

Untuk menguji penjualan atau penghasilan bruto, ketiga teknik (arus uang, arus piutang, arus utang) dapat digabungkan menjadi satu pengujian keterkaitan arus uang dan utang piutang, untuk mendapatkan nilai **tunai dan akrual** penghasilan bruto sekaligus. Strukturnya (source: se65_pj_2013_metode_teknik_pemeriksaan.md):

| Pos | Uraian | Arah |
|-----|--------|------|
| 1a | Penerimaan tunai: penerimaan kas/bank | +/+ |
| 1a | Penerimaan non penghasilan/non objek pajak | -/- |
| 1b | Non tunai: bukti potong/pungut diterima | +/+ |
| 1b | Non tunai: offset utang piutang | +/+ |
| 2a | Saldo awal piutang usaha | -/- |
| 2b | Saldo akhir piutang usaha | +/+ |
| 2c | Saldo awal uang muka pelanggan | +/+ |
| 2d | Saldo akhir uang muka pelanggan | -/- |
| 2e | Saldo awal pendapatan ditangguhkan | +/+ |
| 2f | Saldo akhir pendapatan ditangguhkan | -/- |
| 3 | **Penghasilan bruto termasuk PPN** | +/+ |
| 4 | PPN dipungut sendiri (dari SPT Masa PPN, dikurangi PPN tanpa aliran uang masuk kas/bank dan PPN difakturkan antar waktu) | -/- |
| 5 | **Penghasilan bruto menurut Pemeriksa** | +/+ |
| 6 | Penghasilan bruto menurut SPT Wajib Pajak | -/- |
| 7 | **Selisih** | +/- |

### Hal-hal yang harus diyakini pemeriksa

- **PPN dalam penerimaan**: harus diyakini bahwa di dalam uang yang diterima terkandung PPN; bandingkan dengan PPN dipungut sendiri pada SPT Masa PPN (source: se65_pj_2013_metode_teknik_pemeriksaan.md).
- **PPN yang dikurangkan**: nilai PPN dipungut sendiri dapat diperoleh dari SPT Masa PPN, penelusuran jurnal transaksi PPN, atau mutasi utang PPN pada buku besar. Pastikan tidak termasuk PPN yang tidak terdapat aliran uang ke kas/bank, misalnya PPN yang ditanggung sendiri (pemberian cuma-cuma, pemakaian sendiri, sampel), PPN dipungut beda waktu (faktur diterbitkan lebih dulu, pelunasan belum diterima, atau sebaliknya), dan transaksi lain yang nyata-nyata tidak terdapat titipan PPN dalam penerimaan uang (source: se65_pj_2013_metode_teknik_pemeriksaan.md).
- **Selisih akhir**: harus diyakini merupakan penjualan atau penghasilan lain sebagai tambahan kemampuan ekonomis (source: se65_pj_2013_metode_teknik_pemeriksaan.md).

## Peran masing-masing teknik pengujian keterkaitan

| Teknik | Digunakan untuk mendapatkan |
|--------|-----------------------------|
| Pengujian arus uang | Nilai tunai dari penjualan dan penghasilan bruto |
| Pengujian arus piutang | Nilai pelunasan yang tidak secara tunai |
| Pengujian arus utang | Uang muka penjualan/pelanggan atau penghasilan bruto secara akrual |

(source: se65_pj_2013_metode_teknik_pemeriksaan.md)

## Contoh penghitungan

Dalam SE-65 terdapat contoh penghitungan penghasilan bruto dengan menggabungkan pengujian keterkaitan arus uang dan utang piutang (kasus Wajib Pajak dengan penerimaan reimbursement yang difakturkan Rp5.000.000,00). Alurnya: penerimaan tunai (kas/bank dikurangi penerimaan non penghasilan, termasuk pencairan pinjaman dan penggantian biaya) ditambah penerimaan non tunai (bukti potong PPh Pasal 23, bukti pungut PPh Pasal 22, offset piutang), lalu disesuaikan dengan pos akrual (saldo awal/akhir piutang, uang muka pelanggan, pendapatan ditangguhkan), dikurangi PPN dipungut sendiri, sehingga diperoleh penghasilan bruto menurut Pemeriksa untuk dibandingkan dengan SPT PPh Badan (source: se65_pj_2013_metode_teknik_pemeriksaan.md).

## Related pages

- [[concept/pemeriksaan-pajak/_learning-path|Learning Path: Pemeriksaan Pajak]]
- [[_learning-path|Master Learning Path]]