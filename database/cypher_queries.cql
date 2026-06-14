// 1. Menghapus seluruh data lama (Reset Database)
MATCH (n) DETACH DELETE n;

// 2. Membuat Constraints (Agar pencarian data secepat kilat & tidak ada duplikat)
CREATE CONSTRAINT IF NOT EXISTS FOR (b:Book) REQUIRE b.isbn IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (u:User) REQUIRE u.id IS UNIQUE;

// 3. Logika Import Data Buku (Nodes)
UNWIND $batch AS row
MERGE (b:Book {isbn: row.isbn})
SET b.title = row.title,
    b.author = row.author,
    b.year = row.year,
    b.publisher = row.publisher;

// 4. Logika Import Data Rating (Edges / Relationships)
UNWIND $batch AS row
MERGE (u:User {id: row.user_id})
MERGE (b:Book {isbn: row.isbn})
MERGE (u)-[r:RATED]->(b)
SET r.score = row.rating;