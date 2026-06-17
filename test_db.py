# test_db.py
import psycopg2

try:
    conn = psycopg2.connect(
        database="sekolah_db",
        user="postgres",
        password="password_anda",  # Ganti dengan password asli
        host="localhost",
        port="5432"
    )
    print("Koneksi BERHASIL!")
    conn.close()
except Exception as e:
    print(f"Koneksi GAGAL: {e}")