from neo4j import GraphDatabase

# --- KONFIGURASI DATABASE ---
URI = "neo4j+s://9e428084.databases.neo4j.io"
USER = "9e428084"
PASSWORD = "zHsC2AjO1261e4f-S9BC10LIur_1dkYpF4WBDfkNrr0"

def buat_koneksi():
    try:
        driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
        return driver
    except Exception as e:
        print(f"Error Koneksi: {e}")
        return None

def cari_rekomendasi_buku(judul_buku, limit=5):
    driver = buat_koneksi()
    if not driver:
        return {"error": "Database tidak terhubung. Cek URI dan Password."}

    # Query yang disederhanakan dan lebih stabil
    query = """
    MATCH (b:Book)
    WHERE toLower(b.title) CONTAINS toLower($judul)
    WITH b LIMIT 1
    
    MATCH (u:User)-[:RATED]->(b)
    MATCH (u)-[r2:RATED]->(rekomendasi:Book)
    WHERE rekomendasi.isbn <> b.isbn
    
    RETURN 
        rekomendasi.title AS judul, 
        rekomendasi.author AS penulis, 
        rekomendasi.year AS tahun, 
        rekomendasi.publisher AS penerbit,
        rekomendasi.isbn AS isbn,
        count(u) AS skor_kemiripan,
        round(avg(r2.score), 1) AS rating_rata_rata
    ORDER BY skor_kemiripan DESC
    LIMIT $batas
    """
    
    hasil_rekomendasi = []
    try:
        with driver.session() as session:
            result = session.run(query, judul=judul_buku, batas=limit)
            
            # Memasukkan data dari Neo4j ke Python
            for record in result:
                hasil_rekomendasi.append({
                    "judul": record["judul"],
                    "penulis": record["penulis"],
                    "tahun": record["tahun"],
                    "penerbit": record["penerbit"],
                    "isbn": record["isbn"],
                    "skor": record["skor_kemiripan"],
                    "rating": record["rating_rata_rata"]
                })
                
    except Exception as e:
        # INI KUNCI UTAMANYA: Mengirim pesan error asli ke web agar bisa kita baca!
        pesan_error = str(e)
        print(f"[DEBUG ERROR] {pesan_error}")
        return {"error": pesan_error}
        
    finally:
        driver.close()
        
    return hasil_rekomendasi