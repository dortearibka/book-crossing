import streamlit as st
from backend import cari_rekomendasi_buku

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Sistem Rekomendasi Buku",
    page_icon="📖",
    layout="centered"
)

# --- CUSTOM CSS UNTUK TAMPILAN PREMIUM ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .book-card {
        background-color: #f8fafc;
        border-radius: 15px;
        padding: 25px;
        border: 1px solid #e2e8f0;
        margin-bottom: 20px;
        transition: transform 0.2s;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    .book-card:hover {
        transform: translateY(-5px);
        border-color: #3b82f6;
    }

    .book-title {
        color: #1e293b;
        font-size: 22px;
        font-weight: 700;
        margin-bottom: 10px;
        line-height: 1.3;
    }

    .info-label {
        color: #64748b;
        font-size: 14px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .info-value {
        color: #334155;
        font-size: 16px;
        margin-bottom: 8px;
    }

    .rating-badge {
        background-color: #fef3c7;
        color: #d97706;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 14px;
        display: inline-block;
    }
    
    div.stButton > button:first-child {
        background-color: #2563eb;
        color: white;
        border-radius: 10px;
        width: 100%;
        font-weight: 600;
        border: none;
        padding: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER SECTION ---
st.title("Sistem Rekomendasi Buku")
# REVISI 1: Narasi caption diubah agar lebih fokus ke pengguna
st.caption("Temukan buku bacaan berikutnya yang sesuai dengan seleramu lewat analisis jaringan buku.")
st.write("")

# --- SEARCH SECTION ---
with st.container():
    judul_input = st.text_input(
        "Masukkan judul buku favoritmu (Bahasa Inggris):", 
        placeholder="Contoh: Harry Potter, The Hobbit, 1984...",
        help="Ketik judul buku yang kamu suka, lalu kami akan mencarikan rekomendasinya."
    )
    
    search_clicked = st.button("Cari Rekomendasi")

st.write("---")

# --- LOGIKA PENCARIAN ---
if search_clicked:
    if not judul_input.strip():
        st.warning("Ketikkan judul bukunya dulu, ya.")
    else:
        with st.spinner("Mencari rekomendasi buku terbaik untukmu..."):
            hasil = cari_rekomendasi_buku(judul_input)

        if isinstance(hasil, dict) and "error" in find_recommendations:
            st.error("Gagal terhubung ke database. Cek kembali koneksi Neo4j-nya.")
        elif len(hasil) == 0:
            st.info(f"Belum ada cukup data untuk buku '{judul_input}'. Yuk, coba judul best-seller lain!")
        else:
            # REVISI 2: Menggunakan kalimat rekomendasi yang standar dan netral
            st.subheader(f"Rekomendasi berdasarkan '{judul_input}':")
            st.write("")
            
            for idx, buku in enumerate(hasil, 1):
                st.markdown(f"""
                <div class="book-card">
                    <div class="book-title">{idx}. {buku.get('judul', 'Untitled')}</div>
                    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                        <div style="flex: 1;">
                            <div class="info-label">Penulis</div>
                            <div class="info-value">{buku.get('penulis', '-')}</div>
                            <div class="info-label">Penerbit</div>
                            <div class="info-value">{buku.get('penerbit', '-')}</div>
                        </div>
                        <div style="flex: 1; border-left: 1px solid #e2e8f0; padding-left: 20px;">
                            <div class="info-label">Tahun Terbit</div>
                            <div class="info-value">{buku.get('tahun', '-')}</div>
                            <div class="info-label">ISBN</div>
                            <div class="info-value">{buku.get('isbn', '-')}</div>
                            <div class="rating-badge">⭐ {buku.get('rating', 0)} / 10</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

# --- FOOTER ---
st.write("")
st.caption("© 2024 Project Team • Data source: Book-Crossing Dataset")