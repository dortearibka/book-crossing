from neo4j import GraphDatabase

# --- KONFIGURASI DATABASE ---
# Ganti dengan kredensial Neo4j AuraDB milik Anggota 2
URI = "neo4j+s://9e428084.databases.neo4j.io"
USER = "9e428084"
PASSWORD = "zHsC2AjO1261e4f-S9BC10LIur_1dkYpF4WBDfkNrr0"

def buat_koneksi():
    """Membuka jalur komunikasi ke database Neo4j."""
    try:
        driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
        driver.verify_connectivity()
        return driver
    except Exception as e:
        print(f"[ERROR] Gagal terhubung ke Neo4j: {e}")
        return None

def cari_rekomendasi_buku(judul_buku, limit=5):
    """
    Fungsi inti Knowledge Graph:
    Mencari rekomendasi buku berdasarkan riwayat rating pengguna lain (Collaborative Filtering).
    """
    driver = buat_koneksi()
    if not driver:
        return {"error": "Database tidak terhubung"}

    # Query Cypher yang sangat powerful ini akan melakukan:
    # 1. Mencari buku yang mirip dengan input user (Case Insensitive)
    # 2. Mencari User yang memberi rating di atas 6 untuk buku tersebut
    # 3. Mencari buku lain yang juga diberi rating di atas 6 oleh User tersebut
    # 4. Menghitung buku mana yang paling sering muncul beririsan
    query = """
    MATCH (b:Book)
    WHERE toLower(b.title) CONTAINS toLower($judul)
    WITH b LIMIT 1
    
    MATCH (b)<-[r1:RATED]-(u:User)-[r2:RATED]->(rekomendasi:Book)
    WHERE r1.score > 6 AND r2.score > 6 AND rekomendasi.isbn <> b.isbn
    
    RETURN 
        rekomendasi.title AS judul, 
        rekomendasi.author AS penulis, 
        rekomendasi.year AS tahun, 
        count(u) AS skor_kemiripan
    ORDER BY skor_kemiripan DESC
    LIMIT $batas
    """
    
    hasil_rekomendasi = []
    
    try:
        with driver.session() as session:
            result = session.run(query, judul=judul_buku, batas=limit)
            
            for record in result:
                hasil_rekomendasi.append({
                    "judul": record["judul"],
                    "penulis": record["penulis"],
                    "tahun": record["tahun"],
                    "skor": record["skor_kemiripan"]
                })
                
    except Exception as e:
        print(f"[ERROR] Query bermasalah: {e}")
    finally:
        driver.close()
        
    return hasil_rekomendasi

# --- BAGIAN TESTING (UJI COBA) ---
# Kode di bawah ini hanya akan jalan jika file backend.py di-run langsung di terminal
if __name__ == "__main__":
    print("Mencoba koneksi dan mencari rekomendasi untuk buku 'Harry Potter'...")
    
    # Ingat: Dataset kita berbahasa Inggris, jadi gunakan buku internasional!
    hasil = cari_rekomendasi_buku("Harry Potter")
    
    if isinstance(hasil, dict) and "error" in hasil:
        print("Gagal mengambil data karena error koneksi.")
    elif len(hasil) == 0:
        print("Buku tidak ditemukan atau belum ada data rekomendasi.")
    else:
        print("\n📚 BUKU YANG DIREKOMENDASIKAN UNTUK ANDA:")
        for i, buku in enumerate(hasil, 1):
            print(f"{i}. {buku['judul']} (Karya: {buku['penulis']}, Tahun: {buku['tahun']}) - Skor: {buku['skor']}")