"""Generate working paper ekualisasi PPh Badan vs PPN (omset + pembelian).

Output: working-papers/ekualisasi-pph-ppn.xlsx
Colors (industry standard):
  blue font  = hardcoded input (isi manual)
  black font = formula (otomatis)
  yellow bg  = key cells needing attention
Formula convention: all Totals are =SUM(...), selisih are simple +/-.
Run: python tools/make-ekualisasi-workbook.py
"""
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.formatting.rule import CellIsRule
from openpyxl.utils import get_column_letter

OUT = "working-papers/ekualisasi-pph-ppn.xlsx"

MONTHS = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun",
          "Jul", "Agu", "Sep", "Okt", "Nov", "Des"]
NCOL = len(MONTHS) + 1  # B..M = months, N = Total
TOTCOL = get_column_letter(NCOL + 1)  # N

# colors
BLUE = Font(color="0000FF")
BLACK = Font(color="000000")
BOLD = Font(bold=True)
TITLE = Font(bold=True, size=14)
NOTE = Font(color="808080", italic=True, size=9)
HDR = Font(bold=True, color="FFFFFF")
SEC = Font(bold=True, size=11)
YELLOW = PatternFill("solid", start_color="FFFF00")
GRAY = PatternFill("solid", start_color="D9D9D9")
BLUEFILL = PatternFill("solid", start_color="DDEBF7")
REDFILL = PatternFill("solid", start_color="FFC7CE")
THIN = Border(*[Side(style="thin", color="BFBFBF")] * 4)


def setup_sheet(ws, title):
    ws.merge_cells(f"A1:{TOTCOL}1")
    ws["A1"] = title
    ws["A1"].font = TITLE
    ws.merge_cells(f"A2:{TOTCOL}2")
    ws["A2"] = ("Sumber: SPT Tahunan 1771 (lampiran laba rugi), SPT Masa PPN 1111 (12 masa), buku besar. "
                "Isi sel berhuruf biru; sel hitam = formula otomatis. Tahun pajak di sel kuning.")
    ws["A2"].font = NOTE
    ws.column_dimensions["A"].width = 62
    for i in range(2, 12):
        ws.column_dimensions[get_column_letter(i)].width = 11.5
    ws.column_dimensions[TOTCOL].width = 15
    # header row 4
    ws["A4"] = "POS"
    for i, m in enumerate(MONTHS):
        c = ws.cell(row=4, column=2 + i, value=m)
        c.font = HDR; c.fill = GRAY; c.alignment = Alignment(horizontal="center")
        c.border = THIN
    tc = ws[f"{TOTCOL}4"]; tc.font = HDR; tc.fill = GRAY
    tc.alignment = Alignment(horizontal="center"); tc.border = THIN
    ws["A4"].font = HDR; ws["A4"].fill = GRAY; ws["A4"].border = THIN
    ws.freeze_panes = "B5"
    return 4


def sec(ws, row, text):
    ws.merge_cells(f"A{row}:{TOTCOL}{row}")
    c = ws[f"A{row}"]; c.value = text; c.font = SEC; c.fill = GRAY
    for col in range(2, NCOL + 2):
        ws.cell(row=row, column=col).fill = GRAY
    return row + 1


def inp(ws, row, label):
    ws[f"A{row}"] = label
    ws[f"A{row}"].font = BLACK
    for col in range(2, NCOL + 2):
        c = ws.cell(row=row, column=col)
        c.font = BLUE
        c.number_format = '#,##0;(#,##0);"-"'
        c.border = THIN
    return row + 1


def formula_row(ws, row, label, expr, yellow=False, **fmt):
    """expr template with placeholders {col},{r},{tot} plus any #fmt keys (e.g. a,b)."""
    ws[f"A{row}"] = label
    ws[f"A{row}"].font = BOLD if not yellow else Font(bold=True)
    for ci in range(2, NCOL + 2):
        col = get_column_letter(ci)
        c = ws.cell(row=row, column=ci, value=expr.format(col=col, r=row, tot=TOTCOL, **fmt))
        c.font = BLACK
        c.number_format = '#,##0;(#,##0);"-"'
        c.border = THIN
        if yellow:
            c.fill = YELLOW
    return row + 1


def sum_row(ws, row, label, r1, r2, yellow=False):
    return formula_row(ws, row, label, "=SUM({col}%d:{col}%d)" % (r1, r2), yellow)


def note(ws, row, text):
    ws.merge_cells(f"A{row}:{TOTCOL}{row}")
    ws[f"A{row}"] = text
    ws[f"A{row}"].font = NOTE
    return row + 1


def add_cf(ws, rng):
    ws.conditional_formatting.add(rng, CellIsRule(
        operator="notEqual", formula=["0"],
        fill=REDFILL, font=Font(color="9C0006")))

wb = Workbook()

# ---------------- Sheet: Panduan ----------------
ws = wb.active
ws.title = "Panduan"
ws.column_dimensions["A"].width = 110
guide = [
    ("WORKING PAPER EKUALISASI PPh BADAN & PPN", TITLE),
    ("", NOTE),
    ("TUJUAN", SEC),
    ("Memastikan konsistensi angka antara SPT Tahunan PPh Badan (1771) dan SPT Masa PPN (1111) untuk satu tahun pajak, "
     "di dua sisi: (1) omset/peredaran usaha, (2) pembelian/beban. Selisih yang tidak dapat dijelaskan = indikasi "
     "penghasilan tidak dilaporkan, Pajak Masukan fiktif, atau pemotongan PPh 23/22 kurang.", BLACK),
    ("", NOTE),
    ("CARA PAKAI", SEC),
    ("1. Isi tahun pajak pada sheet Omset & Pembelian (sel kuning).", BLACK),
    ("2. Isi semua sel BIRU: angka dari SPT/laporan laba rugi/buku besar per masa pajak. Total (kolom N) dan "
     "selisih (baris kuning) otomatis terhitung.", BLACK),
    ("3. Isi POS ANALISIS SELISIH untuk menjelaskan selisih. Aturan tanda: + bila pos hanya muncul di sisi PPh "
     "(mengurangi selisih); - bila pos hanya muncul di sisi PPN (menambah selisih).", BLACK),
    ("4. Selisih setelah penyesuaian (baris kuning) diharapkan = 0 atau dapat dijelaskan. Jika tidak, periksa "
     "penyebabnya — sel akan berubah MERAH bila tidak nol.", BLACK),
    ("", NOTE),
    ("LEGENDA WARNA", SEC),
    ("Biru = input manual | Hitam = formula otomatis | Kuning = sel kunci (perhatikan) | Merah = selisih belum dijelaskan", BLACK),
    ("", NOTE),
    ("PENYEBAB SELISIH UMUM — OMSET", SEC),
    ("- Penghasilan bukan penjualan: bunga, jasa giro, dividen, laba selisih kurs (ada di PPh, tidak kena PPN)", BLACK),
    ("- Penjualan kena PPh final: sewa tanah/bangunan, jasa konstruksi, pengalihan tanah/bangunan", BLACK),
    ("- Ekspor: PPN 0% tetap dilaporkan di SPT Masa PPN, masuk peredaran usaha PPh", BLACK),
    ("- DPP nilai lain / faktur digunggung (penjualan eceran) → angka DPP berbeda dari harga jual", BLACK),
    ("- Pemakaian sendiri / pemberian cuma-cuma: kena PPN tapi bukan penjualan di laba rugi", BLACK),
    ("- Retur, diskon, penyesuaian harga; uang muka pelanggan; beda masa terbitnya faktur", BLACK),
    ("", NOTE),
    ("PENYEBAB SELISIH UMUM — PEMBELIAN", SEC),
    ("- Pembelian dari non-PKP / pedagang eceran: Pajak Masukan tidak ada / digunggung", BLACK),
    ("- Pajak Masukan tidak dapat dikreditkan (Pasal 9(8) UU PPN / PMK 18/2021: sedan, makanan-minuman, dll)", BLACK),
    ("- Beban tanpa PPN: gaji, bunga, PPh, denda, asuransi", BLACK),
    ("- Impor: PPN impor via SSP", BLACK),
    ("- Uang muka pembelian (beda waktu); capex (DPP PM penuh) vs penyusutan (beban PPh bertahap)", BLACK),
    ("- PM dikreditkan tanpa pembelian di laba rugi = indikasi PM bermasalah", BLACK),
    ("", NOTE),
    ("CATATAN & STATUS", SEC),
    ("Working paper ini adalah alat bantu (draft, belum diverifikasi sumber resmi). Acuan teknik pengujian: "
     "SE-65/PJ/2013. Tarif PPN 12% dengan DPP 11/12 untuk sebagian besar penyerahan (PMK 131/2024 jo PMK 11/2025).", NOTE),
]
r = 1
for text, fnt in guide:
    ws.cell(row=r, column=1, value=text).font = fnt
    if fnt is SEC:
        ws.cell(row=r, column=1).fill = GRAY
    r += 1

# ---------------- Sheet: Omset ----------------
ws = wb.create_sheet("Omset")
r = setup_sheet(ws, "EKUALISASI OMSET — PPh Badan vs PPN (sisi penjualan)")
ws["A2"] = "Tahun pajak:"  # overwrite note line? keep note; add year cell below
ws["A3"] = "Tahun pajak:"; ws["A3"].font = BLACK
ws["B3"] = 2026; ws["B3"].font = BLUE; ws["B3"].fill = YELLOW
ws["B3"].number_format = "0"
r = 4  # header row written by setup_sheet
r = 5
r = sec(ws, r, "OMSET / PEREDARAN USAHA — SISI PPh")
r1 = r  # 6
r = inp(ws, r, "1. Penjualan neto — laporan laba rugi (1771)")
r = inp(ws, r, "2. Koreksi fiskal atas penjualan (+/-)")
r1e = r - 1
r = sum_row(ws, r, "3. = Peredaran usaha fiskal", r1, r1e)
row3 = r - 1
r = inp(ws, r, "4. Omzet PPN — total DPP SPT Masa PPN (terutang + tidak terutang + ekspor)")
row4 = r - 1
r = formula_row(ws, r, "5. Selisih awal (3 - 4)", "={col}{a}-{col}{b}", a=row3, b=row4)
row5 = r - 1
r += 1
r = sec(ws, r, "POS ANALISIS SELISIH (isi +/-; + = hanya di sisi PPh, - = hanya di sisi PPN)")
items = [
    "6a. Penghasilan lain bukan penjualan (bunga, jasa giro, dividen, laba kurs, dll)",
    "6b. Penjualan kena PPh final (sewa tanah/bangunan, jasa konstruksi, pengalihan tanah/bangunan)",
    "6c. Ekspor (penyerahan PPN 0% - cek kesesuaian)",
    "6d. Perbedaan DPP (DPP nilai lain, penjualan eceran / faktur digunggung)",
    "6e. Pemakaian sendiri / pemberian cuma-cuma (kena PPN, bukan penjualan)",
    "6f. Retur, diskon, penyesuaian harga",
    "6g. Uang muka pelanggan (beda waktu pengakuan)",
    "6h. Beda masa penyerahan (faktur diterbitkan di masa berbeda)",
    "6i. Lain-lain (jelaskan di catatan)",
]
r_items = []
for it in items:
    r_items.append(r)
    r = inp(ws, r, it)
r = sum_row(ws, r, "7. Total penyesuaian", r_items[0], r_items[-1])
row7 = r - 1
r = formula_row(ws, r, "8. Selisih setelah penyesuaian (5 - 7) — harus 0/dapat dijelaskan",
                "={col}{a}-{col}{b}", a=row5, b=row7, yellow=True)
add_cf(ws, f"B{r-1}:{TOTCOL}{r-1}")
r = note(ws, r + 1, "Selisih > 0 = ada penghasilan di PPh yang tidak dilaporkan ke PPN (atau sebaliknya - check tanda); "
                    "Selisih < 0 = kelebihan pelaporan / beda DPP. Jelaskan di pos analisis.")

# ---------------- Sheet: Pembelian ----------------
ws = wb.create_sheet("Pembelian")
r = setup_sheet(ws, "EKUALISASI PEMBELIAN — PPh Badan vs PPN (sisi pembelian/beban)")
ws["A2"] = "Tahun pajak:"
ws["A3"] = "Tahun pajak:"; ws["A3"].font = BLACK
ws["B3"] = 2026; ws["B3"].font = BLUE; ws["B3"].fill = YELLOW
ws["B3"].number_format = "0"
r = 5
r = sec(ws, r, "PEMBELIAN / BEBAN — SISI PPh")
r1 = r
r = inp(ws, r, "1. Pembelian barang dagangan & bahan baku (HPP) - laporan laba rugi")
r = inp(ws, r, "2. Beban jasa & biaya operasional lainnya")
r = inp(ws, r, "3. Perolehan aset (capex)")
r = inp(ws, r, "4. Koreksi fiskal atas beban (+/-)")
r1e = r - 1
r = sum_row(ws, r, "5. = Total pembelian/beban fiskal", r1, r1e)
row5 = r - 1
r = inp(ws, r, "6. DPP Pajak Masukan yang dikreditkan - SPT Masa PPN 1111")
row6 = r - 1
r = formula_row(ws, r, "7. Selisih awal (5 - 6)", "={col}{a}-{col}{b}", a=row5, b=row6)
row7 = r - 1
r += 1
r = sec(ws, r, "POS ANALISIS SELISIH (isi +/-; + = ada beban PPh tanpa PM, - = ada PM tanpa beban)")
items = [
    "8a. Pembelian dari non-PKP / pedagang eceran (PM tidak ada / digunggung)",
    "8b. PM tidak dapat dikreditkan (Pasal 9(8) UU PPN / PMK 18/2021: sedan, makanan-minuman, dll)",
    "8c. Beban tanpa PPN (gaji, bunga, PPh, denda, asuransi)",
    "8d. Impor (PPN impor via SSP)",
    "8e. Uang muka pembelian (beda waktu)",
    "8f. Beda aset: capex (DPP PM penuh) vs penyusutan (beban PPh bertahap)",
    "8g. PM dikreditkan tanpa pembelian di laba rugi (indikasi PM bermasalah)",
    "8h. PM belum dikreditkan / tidak dilaporkan (retur, PM kolektif)",
    "8i. Lain-lain (jelaskan di catatan)",
]
r_items = []
for it in items:
    r_items.append(r)
    r = inp(ws, r, it)
r = sum_row(ws, r, "9. Total penyesuaian", r_items[0], r_items[-1])
row9 = r - 1
r = formula_row(ws, r, "10. Selisih setelah penyesuaian (7 - 9) — harus 0/dapat dijelaskan",
                "={col}{a}-{col}{b}", a=row7, b=row9, yellow=True)
add_cf(ws, f"B{r-1}:{TOTCOL}{r-1}")
r = note(ws, r + 1, "Selisih > 0 = beban PPh tanpa Pajak Masukan (umum; jelaskan pos). "
                    "Selisih < 0 = Pajak Masukan dikreditkan tanpa beban di laba rugi = indikasi masalah (periksa).")

import os
os.makedirs(os.path.dirname(OUT), exist_ok=True)
wb.save(OUT)
n_formulas = 0
for s in wb:
    for row in s.iter_rows():
        for c in row:
            if isinstance(c.value, str) and c.value.startswith("="):
                n_formulas += 1
print(f"saved {OUT}; sheets: {wb.sheetnames}; formulas: {n_formulas}")