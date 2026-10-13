# datafactor - Reverse Engineering 🛡️🔍

Selamat datang di sub-project **datafactor** yang berfokus pada **Reverse Engineering**. Repositori ini digunakan untuk mendokumentasikan proses analisis, pembedahan sistem (binary/software), eksperimen dekompilasi, serta riset keamanan siber secara mendalam.

## 📁 Struktur Folder
* `/binaries` : Tempat menyimpan sampel file binary atau aplikasi yang dianalisis (pastikan aman/bukan malware aktif).
* `/docs` : Dokumentasi hasil analisis statis, dinamis, alur kerja (control flow graph), dan temuan penting.
* `/scripts` : Script otomatisasi penunjang (Python, Frida scripts, atau IDAPython).
* `/tools` : Catatan konfigurasi atau plugin untuk perangkat lunak reverse engineering.

## 🛠️ Tools yang Digunakan
Kami menggunakan beberapa industri-standar tools berikut untuk analisis:
* **Ghidra** – Analisis binary statis & dekompilator buatan NSA.
* **x64dbg / GDB** – Debugging dinamis untuk Windows & Linux.
* **IDA Pro** – Disassembler dan debugger tingkat lanjut.
* **Frida** – Dynamic Binary Instrumentation untuk inspeksi runtime.

## 🚀 Alur Kerja Analisis
1. **Analisis Awal:** Memeriksa arsitektur file (x86, x64, ARM) dan proteksi file (packing/obfuscation).
2. **Disassemble & Decompile:** Membedah biner menjadi assembly atau pseudo-code agar bisa dibaca manusia.
3. **Debugging Dinamis:** Memantau jalannya program secara real-time untuk memvalidasi logika.
4. **Dokumentasi & Kesimpulan:** Mencatat celah keamanan, struktur data, atau merekonstruksi kode asal.

---
*Catatan: Semua aktivitas dalam proyek ini ditujukan untuk tujuan edukasi, riset keamanan, dan pemahaman sistem (interoperabilitas) secara legal.*
