# 📚 Sistem Rekomendasi Buku (Book-Crossing Knowledge Graph)

Proyek ini adalah implementasi Sistem Rekomendasi berbasis Semantic Web / Knowledge Graph menggunakan dataset Book-Crossing dan Neo4j.

## 👥 Anggota Kelompok & Pembagian Tugas

1. **DORTEA RIBKA TADETE** - Data Engineer (Fokus pada `scripts/data_cleaning.py`)
2. **JUSTISYA INJILIA TUMBEL** - Knowledge Graph Engineer (Fokus pada `database/cypher_queries.cql` & Neo4j)
3. **DELAFANNY INSERNBO RUMBIAK** - Backend Developer (Fokus pada `backend.py`)
4. **JONATHAN BILLY PESSAK** - Frontend Developer (Fokus pada `app.py`)

---

## 📂 Penjelasan Struktur Folder & File

- 📁 **`dataset/`** : Tempat menyimpan file CSV yang sudah bersih dan ringan.
- 📁 **`scripts/`** : Tempat menyimpan kode Python untuk membersihkan data mentah.
- 📁 **`database/`** : Tempat menyimpan rancangan relasi graf dan logika bahasa Cypher.
- 📄 **`app.py`** : Kode utama antarmuka web pengguna (UI) menggunakan Streamlit.
- 📄 **`backend.py`** : Kode logika penghubung Streamlit dengan database Neo4j.
- 📄 **`requirements.txt`** : Daftar library Python yang harus di-install.
- 📄 **`.gitignore`** : File konfigurasi pelindung kredensial dan data mentah.

---

## 🚀 Cara Menjalankan Aplikasi

1. Buka terminal dan pastikan berada di folder project ini.
2. Install library yang dibutuhkan dengan perintah: `pip install -r requirements.txt`
3. Jalankan aplikasi web dengan perintah: `streamlit run app.py`
