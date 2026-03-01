# Calf-Hackaton
# 📊 Merchant Dashboard - Financial Intelligence Platform
**Hackathon Project by Team Calf**

Merchant dashboard adalah sebuah platform yang dapat mengintegrasikan ai based Technology untuk data analysis, fraud Detection, predictions, insights, dan recomendation berbasis Ai

## 🚀 Fitur Utama
* **Overview Dashboard**: Visualisasi finansial real-time.
* **AI Recommendations**: Strategi bisnis otomatis via Qwen AI.
* **Fraud Detection**: Deteksi anomali transaksi.
* **Cashflow Prediction**: Proyeksi arus kas 30 hari ke depan.

## 🛠️ Cara Menjalankan
Terdapat dua cara untuk menjalankan aplikasi ini:

### 1. Pengguna Windows (Rekomendasi)
Untuk menjalankan aplikasi secara otomatis tanpa konfigurasi manual:

1. Pastikan Python sudah terinstal di sistem Anda.

2. Lakukan double-click pada file run_app.bat.

3. Script ini akan otomatis menginstal library yang dibutuhkan (pip install -r requirements.txt) dan menjalankan server Backend serta Frontend secara bersamaan.

### 2. Manual / OS Lain (macOS/Linux)
1. Instal library: `pip install -r requirements.txt`
2. Jalankan: `python main.py`

## ☁️ Konfigurasi Server
saat ini dasbor masih diakses melalui local server, tetapi untuk backend sudah di deploy di dalam alibaba cloud ECS
Jika Anda ingin menguji koneksi dashboard langsung ke server cloud (ECS):

1. Buka file Frontend/app.py.

2. Cari bagian konfigurasi BASE_URL.

3. Ubah pilihan ke ECS Server URL (http://8.215.205.66:8000) dengan menghapus tanda komentar (#) dan memberikan komentar pada baris local server.

## Catatan:
Untuk detail teknis lebih lajut dapat diaksek melalui notes.txt

#
© 2026 Tim Calf - Merchant Dashboard Hackathon Project
#