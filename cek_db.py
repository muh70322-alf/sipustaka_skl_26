import sqlite3
import os

db_path = 'db.sqlite3'

if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Cek semua tabel
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Tabel yang ada:", tables)
    
    # Cek struktur tabel buku
    cursor.execute("PRAGMA table_info(buku)")
    columns = cursor.fetchall()
    print("\nKolom di tabel buku:")
    for col in columns:
        print(f"  - {col[1]} ({col[2]})")
    
    conn.close()
else:
    print("Database belum ada, jalankan migrate dulu")