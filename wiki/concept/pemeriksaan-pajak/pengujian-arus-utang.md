---
title: Pengujian Arus Utang
tags: [concept, pemeriksaan-pajak]
date: 2026-08-26
sources: [se65_pj_2013_metode_teknik_pemeriksaan.md]
aliases: [Arus Utang, Payables Flow Test, Pengujian Utang Usaha]
status: stable
chapter: pemeriksaan-pajak
difficulty: intermediate
estimated_minutes: 20
---
# Pengujian Arus Utang

**Summary**: Teknik pemeriksaan yang menyusun mutasi akun utang untuk meyakini pos yang diuji — pembelian barang secara kredit (arus utang usaha), penerimaan pinjaman (arus utang bank/afiliasi/pemegang saham), atau penjualan yang sebelumnya diterima sebagai uang muka pelanggan (source: se65_pj_2013_metode_teknik_pemeriksaan.md).

---

## Tujuan dan prinsip pemilihan akun

Pengujian arus utang **tergantung kepada pos yang akan diyakini kebenarannya** (source: se65_pj_2013_metode_teknik_pemeriksaan.md):

- Untuk meyakini **pembelian barang secara kredit** → pengujian **arus utang usaha** (accounts payable);
- Untuk meyakini **penerimaan pinjaman** → pengujian **arus utang bank/afiliasi/pemegang saham**;
- Untuk meyakini **uang muka penjualan/pelanggan** → pemeriksaan atas penjualan/pendapatan yang sebelumnya berupa uang muka.

Terhubung dengan [[pengujian-arus-uang]] (sumber pembelian tunai dan pelunasan utang) dan [[pengujian-arus-piutang]] (sisi piutang pada pengujian gabungan).

## Formula pembelian (arus utang usaha)

```
Saldo Akhir Utang Usaha        +/+
Pembelian Tunai                +/+
Pelunasan Utang Usaha          +/+
Saldo Awal Utang Usaha         -/-
Penyesuaian                    +/-
-----------------------------------
Pembelian                      xxx
```

(source: se65_pj_2013_metode_teknik_pemeriksaan.md)

**Logika**: kenaikan utang usaha selama setahun (saldo akhir − saldo awal) berasal dari pembelian kredit yang belum dibayar; pelunasan yang keluar dari kas/bank menunjukkan pembelian kredit yang sudah terbayar. Jadi pembelian kredit = (saldo akhir − saldo awal) + pelunasan; tambahkan pembelian tunai (dari [[pengujian-arus-uang]]) untuk total pembelian.

**Penyesuaian wajib**: formula harus memperhatikan transaksi dalam mutasi utang usaha yang **tidak terkait pembelian**, seperti utang karena biaya (utang gaji, utang PPh, utang PPN), salah posting, offset utang-piutang, dan sebagainya (source: se65_pj_2013_metode_teknik_pemeriksaan.md).

## Formula uang muka penjualan/pelanggan

```
Saldo Awal Uang Muka Penjualan/Pelanggan    +/+
Penambahan Uang Muka Penjualan/Pelanggan    +/+
Saldo Akhir Uang Muka Penjualan/Pelanggan   -/-
Penyesuaian                                 +/-
-----------------------------------------------
Penjualan/Pendapatan terkait Uang Muka      xxx
```

(source: se65_pj_2013_metode_teknik_pemeriksaan.md)

## Langkah praktis menyusun arus utang (untuk menguji pembelian)

1. Ambil **mutasi akun utang usaha** dari buku besar: saldo awal, mutasi debit/kredit, saldo akhir.
2. Telusuri **pelunasan utang** = mutasi kas/bank yang terkait pembayaran ke pemasok (bukti bank, cek/giro).
3. **Saring penyesuaian** — buang semua mutasi utang yang tidak terkait pembelian (utang biaya, salah posting, offset).
4. Tambahkan **pembelian tunai** dari hasil [[pengujian-arus-uang]].
5. Bandingkan hasil dengan **pembelian menurut SPT Wajib Pajak** — selisih berimplikasi pada PPh 23/22 yang kurang dipotong dan Pajak Masukan yang tidak sah dikreditkan.

## Contoh perhitungan

| Pos | Nilai |
|---|---:|
| Saldo awal utang usaha | 100 |
| Saldo akhir utang usaha | 150 |
| Pelunasan utang usaha (mutasi debet kas/bank ke pemasok) | 400 |
| Pembelian tunai | 50 |
| **Pembelian kredit** = 150 + 400 − 100 | **450** |
| **Total pembelian** = 450 + 50 | **500** |

(contoh ilustratif)

## Posisi dalam pengujian keterkaitan

| Teknik | Digunakan untuk mendapatkan |
|--------|-----------------------------|
| [[pengujian-arus-uang\|Pengujian arus uang]] | Nilai **tunai** dari penjualan dan penghasilan bruto |
| [[pengujian-arus-piutang\|Pengujian arus piutang]] | Nilai pelunasan **non-tunai** |
| **Pengujian arus utang** | **Uang muka penjualan/pelanggan** atau penghasilan bruto secara **akrual** |

(source: se65_pj_2013_metode_teknik_pemeriksaan.md)

Mengingat perkembangan bisnis dan akuntansi, ketiga teknik dapat saling mendukung dalam menguji kebenaran suatu pos SPT — digabungkan menjadi pengujian atas **arus uang dan utang-piutang** untuk mendapatkan nilai tunai dan akrual penghasilan bruto (lihat grid pos 1a–7 pada [[pengujian-arus-piutang]]).

## Related pages

- [[pengujian-arus-uang]]
- [[pengujian-arus-piutang]]
- [[concept/pemeriksaan-pajak/_learning-path|Learning Path: Pemeriksaan Pajak]]
- [[_learning-path|Master Learning Path]]
