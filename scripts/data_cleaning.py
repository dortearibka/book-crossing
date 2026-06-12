import pandas as pd
import os


def clean_book_crossing():
    # Lokasi folder root project (satu level di atas folder scripts/)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    file_books   = os.path.join(base_dir, "BX-Books.csv")
    file_ratings = os.path.join(base_dir, "BX-Book-Ratings.csv")

    try:
        print("Membaca dataset...")

        df_books = pd.read_csv(file_books, sep=",", encoding="latin-1",
                               on_bad_lines="skip", low_memory=False)
        df_ratings = pd.read_csv(file_ratings, sep=",", encoding="latin-1",
                                 on_bad_lines="skip", low_memory=False)

        # Hapus spasi dan tanda kutip tersembunyi dari nama kolom
        df_books.columns   = df_books.columns.str.strip().str.replace('"', "")
        df_ratings.columns = df_ratings.columns.str.strip().str.replace('"', "")

        # Ambil hanya kolom yang dibutuhkan
        df_books = df_books[
            ["ISBN", "Book-Title", "Book-Author", "Year-Of-Publication", "Publisher"]
        ].copy()


        print("Membersihkan data buku...")

        # Hapus baris yang ada kolom kosong (NaN)
        df_books.dropna(subset=["ISBN", "Book-Title", "Book-Author",
                                 "Year-Of-Publication", "Publisher"], inplace=True)

        # Hapus ISBN yang muncul lebih dari sekali, simpan yang pertama
        df_books.drop_duplicates(subset=["ISBN"], keep="first", inplace=True)

        # Hapus spasi berlebih di awal/akhir teks
        df_books["Book-Title"]  = df_books["Book-Title"].astype(str).str.strip()
        df_books["Book-Author"] = df_books["Book-Author"].astype(str).str.strip()
        df_books["Publisher"]   = df_books["Publisher"].astype(str).str.strip()

        # Konversi tahun ke angka, lalu buang yang di luar rentang 1901-2025
        # (data asli banyak mengandung nilai 0 dan tahun fiktif seperti 2050)
        df_books["Year-Of-Publication"] = pd.to_numeric(
            df_books["Year-Of-Publication"], errors="coerce"
        )
        df_books = df_books[
            (df_books["Year-Of-Publication"] > 1900) &
            (df_books["Year-Of-Publication"] <= 2025)
        ]
        df_books["Year-Of-Publication"] = df_books["Year-Of-Publication"].astype(int)

        # Buang penulis yang tidak informatif
        # (hasil inspeksi data: hanya 'Unknown' dan 'Various' yang perlu dibuang)
        penulis_tidak_valid = {"Unknown", "Various"}
        df_books = df_books[
            ~df_books["Book-Author"].isin(penulis_tidak_valid) &
            (df_books["Book-Author"].str.len() > 1)
        ]


        print("Membersihkan data ratings...")

        # Hapus baris NaN (sangat sedikit, kurang dari 10 baris)
        df_ratings.dropna(inplace=True)

        # Buang rating 0 — artinya user hanya melihat buku, belum memberi nilai
        df_ratings = df_ratings[df_ratings["Book-Rating"] > 0]
        df_ratings["Book-Rating"] = df_ratings["Book-Rating"].astype(int)


        print("Mengambil 5.000 buku paling banyak dirating...")

        # Sinkronkan: hanya proses rating untuk buku yang lolos pembersihan
        isbn_valid   = set(df_books["ISBN"].unique())
        ratings_sync = df_ratings[df_ratings["ISBN"].isin(isbn_valid)]

        # Pilih 5.000 ISBN dengan jumlah rating terbanyak
        top_isbn = ratings_sync["ISBN"].value_counts().nlargest(5000, keep="first").index

        clean_books   = df_books[df_books["ISBN"].isin(top_isbn)].reset_index(drop=True)
        clean_ratings = ratings_sync[ratings_sync["ISBN"].isin(top_isbn)].reset_index(drop=True)


        # Simpan hasil ke folder dataset/
        out_dir = os.path.join(base_dir, "dataset")
        os.makedirs(out_dir, exist_ok=True)

        clean_books.to_csv(os.path.join(out_dir, "Clean_Books.csv"), index=False)
        clean_ratings.to_csv(os.path.join(out_dir, "Clean_Ratings.csv"), index=False)

        print("\nSelesai!")
        print(f"  Buku   : {len(clean_books):,} baris  →  dataset/Clean_Books.csv")
        print(f"  Rating : {len(clean_ratings):,} baris  →  dataset/Clean_Ratings.csv")
        print(f"  User   : {clean_ratings['User-ID'].nunique():,} user unik")

    except FileNotFoundError:
        print("ERROR: File CSV tidak ditemukan.")
        print("Pastikan BX-Books.csv dan BX-Book-Ratings.csv ada di folder book-crossing/")
    except KeyError as e:
        print(f"ERROR: Kolom {e} tidak ditemukan. Cek nama kolom di file CSV.")
    except Exception as e:
        print(f"ERROR: {e}")


if __name__ == "__main__":
    clean_book_crossing()