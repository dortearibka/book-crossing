import pandas as pd
import os
from neo4j import GraphDatabase

# --- KONFIGURASI DATABASE ---
URI = "neo4j+s://9e428084.databases.neo4j.io"
USER = "9e428084"
PASSWORD = "zHsC2AjO1261e4f-S9BC10LIur_1dkYpF4WBDfkNrr0"

def cek_integritas_data():
    print("Memulai proses verifikasi data...\n")
    
    # 1. MENGHITUNG DATA DI CSV LOKAL
    folder_utama = os.path.dirname(os.path.abspath(__file__))
    file_buku = os.path.join(folder_utama, "dataset", "Clean_Books.csv")
    file_rating = os.path.join(folder_utama, "dataset", "Clean_Ratings.csv")
    
    try:
        df_buku = pd.read_csv(file_buku)
        df_rating = pd.read_csv(file_rating)
        
        total_buku_csv = len(df_buku)
        total_rating_csv = len(df_rating)
        total_user_csv = df_rating['User-ID'].nunique()
        
    except Exception as e:
        print(f"Gagal membaca CSV: {e}")
        return

    # 2. MENGHITUNG DATA DI NEO4J (CLOUD)
    try:
        driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
        with driver.session() as session:
            # Menghitung jumlah Node Buku
            result_buku = session.run("MATCH (b:Book) RETURN count(b) AS total")
            total_buku_neo = result_buku.single()["total"]
            
            # Menghitung jumlah Relationship Rating
            result_rating = session.run("MATCH ()-[r:RATED]->() RETURN count(r) AS total")
            total_rating_neo = result_rating.single()["total"]
            
            # Menghitung jumlah Node User
            result_user = session.run("MATCH (u:User) RETURN count(u) AS total")
            total_user_neo = result_user.single()["total"]
            
        driver.close()
    except Exception as e:
        print(f"Gagal terhubung ke Neo4j: {e}")
        return

    # 3. MENAMPILKAN HASIL PERBANDINGAN
    print("="*50)
    print("📊 LAPORAN INTEGRITAS DATA (DATA INTEGRITY CHECK)")
    print("="*50)
    
    print(f"{'Metrik':<20} | {'Di CSV Lokal':<12} | {'Di Neo4j Aura':<12}")
    print("-" * 50)
    print(f"{'Total Buku (Node)':<20} | {total_buku_csv:<12} | {total_buku_neo:<12}")
    print(f"{'Total User (Node)':<20} | {total_user_csv:<12} | {total_user_neo:<12}")
    print(f"{'Total Rating (Edge)':<20} | {total_rating_csv:<12} | {total_rating_neo:<12}")
    print("-" * 50)
    
    # Validasi Otomatis
    if (total_buku_csv == total_buku_neo) and (total_rating_csv == total_rating_neo):
        print("\n✅ KESIMPULAN: STATUS AMAN! Data tersinkronisasi 100%.")
    else:
        print("\n⚠️ KESIMPULAN: ADA SELISIH DATA! Proses import mungkin terputus di tengah jalan.")
    print("="*50)

if __name__ == "__main__":
    cek_integritas_data()