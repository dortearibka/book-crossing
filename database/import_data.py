import pandas as pd
import os
from neo4j import GraphDatabase

# --- KONFIGURASI DATABASE NEO4J ---
URI = "neo4j+s://9e428084.databases.neo4j.io"
USER = "9e428084"
PASSWORD = "zHsC2AjO1261e4f-S9BC10LIur_1dkYpF4WBDfkNrr0"

def buat_constraint(driver):
    print("Membuat aturan constraint di Neo4j...")
    with driver.session() as session:
        session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (b:Book) REQUIRE b.isbn IS UNIQUE;")
        session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (u:User) REQUIRE u.id IS UNIQUE;")

def upload_buku(driver, file_path):
    print("Mengunggah data buku ke Neo4j (Node: Book)...")
    df = pd.read_csv(file_path)
    
    # Mengubah dataframe menjadi daftar dictionary (JSON) agar mudah dibaca Neo4j
    data_buku = []
    for _, row in df.iterrows():
        data_buku.append({
            "isbn": row["ISBN"],
            "title": row["Book-Title"],
            "author": row["Book-Author"],
            "year": int(row["Year-Of-Publication"]),
            "publisher": str(row["Publisher"])
        })
    
    # Upload data secara massal (Batching) menggunakan Cypher UNWIND
    query = """
    UNWIND $batch AS row
    MERGE (b:Book {isbn: row.isbn})
    SET b.title = row.title,
        b.author = row.author,
        b.year = row.year,
        b.publisher = row.publisher
    """
    with driver.session() as session:
        session.run(query, batch=data_buku)

def upload_rating(driver, file_path):
    print("Mengunggah data rating ke Neo4j (Relationship: RATED)...")
    df = pd.read_csv(file_path)
    
    data_rating = []
    for _, row in df.iterrows():
        data_rating.append({
            "user_id": int(row["User-ID"]),
            "isbn": row["ISBN"],
            "rating": int(row["Book-Rating"])
        })
    
    query = """
    UNWIND $batch AS row
    MERGE (u:User {id: row.user_id})
    WITH u, row
    MATCH (b:Book {isbn: row.isbn})
    MERGE (u)-[r:RATED]->(b)
    SET r.score = row.rating
    """
    with driver.session() as session:
        session.run(query, batch=data_rating)

def main():
    print("Memulai proses injeksi data ke Neo4j...")
    folder_utama = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_buku = os.path.join(folder_utama, "dataset", "Clean_Books.csv")
    file_rating = os.path.join(folder_utama, "dataset", "Clean_Ratings.csv")

    try:
        # Membuka koneksi ke database Neo4j
        driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
        driver.verify_connectivity()
        print("✅ Berhasil terhubung ke Neo4j AuraDB!")
        
        buat_constraint(driver)
        upload_buku(driver, file_buku)
        upload_rating(driver, file_rating)
        
        print("✅ SUKSES! Seluruh data berhasil membentuk Knowledge Graph di Neo4j.")
        driver.close()
        
    except Exception as e:
        print(f"❌ Terjadi kesalahan koneksi atau upload: {e}")

if __name__ == "__main__":
    main()