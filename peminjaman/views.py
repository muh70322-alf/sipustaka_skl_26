from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import connection
from datetime import date, timedelta

def dashboard(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT SUM(stok) FROM buku")
            result = cursor.fetchone()
            total_buku = result[0] if result and result[0] else 0
            
            cursor.execute("SELECT COUNT(*) FROM buku")
            result = cursor.fetchone()
            total_judul = result[0] if result else 0
            
            cursor.execute("SELECT COUNT(*) FROM peminjaman WHERE status = 'Dipinjam'")
            result = cursor.fetchone()
            sedang_dipinjam = result[0] if result else 0
            
            cursor.execute("SELECT COUNT(*) FROM peminjaman WHERE status = 'Dikembalikan'")
            result = cursor.fetchone()
            sudah_dikembalikan = result[0] if result else 0
            
            cursor.execute("SELECT judul, stok FROM buku ORDER BY stok DESC LIMIT 10")
            stok_buku_data = cursor.fetchall()
            
            cursor.execute("SELECT MAX(stok) FROM buku")
            max_result = cursor.fetchone()
            max_stok = max_result[0] if max_result and max_result[0] else 1
            
    except Exception as e:
        print(f"Error dashboard: {e}")
        total_buku = total_judul = sedang_dipinjam = sudah_dikembalikan = 0
        stok_buku_data = []
        max_stok = 1
    
    stok_list = []
    for s in stok_buku_data:
        persentase = int((s[1] / max_stok) * 100) if max_stok > 0 else 0
        stok_list.append({
            'judul': s[0], 
            'stok': s[1],
            'persen': persentase
        })
    
    context = {
        'total_buku': total_buku,
        'total_judul': total_judul,
        'sedang_dipinjam': sedang_dipinjam,
        'sudah_dikembalikan': sudah_dikembalikan,
        'stok_buku': stok_list,
    }
    return render(request, 'dashboard.html', context)


def peminjaman_create(request):
    today = date.today()
    jatuh_tempo_default = today + timedelta(days=7)
    
    if request.method == 'POST':
        siswa_id = request.POST.get('siswa_id')
        buku_id = request.POST.get('buku_id')
        tanggal_pinjam = request.POST.get('tanggal_pinjam')
        jatuh_tempo = request.POST.get('jatuh_tempo')
        keperluan = request.POST.get('keperluan')
        catatan = request.POST.get('catatan', '')
        
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT stok FROM buku WHERE id = %s", [buku_id])
                stok_result = cursor.fetchone()
                
                if stok_result and stok_result[0] > 0:
                    cursor.execute("UPDATE buku SET stok = stok - 1 WHERE id = %s", [buku_id])
                    cursor.execute("""
                        INSERT INTO peminjaman (siswa_id, buku_id, tanggal_pinjam, jatuh_tempo, keperluan, catatan, petugas, status)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, 'Dipinjam')
                    """, [siswa_id, buku_id, tanggal_pinjam, jatuh_tempo, keperluan, catatan, 'Budi Siregar'])
                    messages.success(request, 'Buku berhasil dipinjam!')
                    return redirect('peminjaman_list')
                else:
                    messages.error(request, 'Stok buku tidak mencukupi!')
        except Exception as e:
            print(f"Error peminjaman_create: {e}")
            messages.error(request, f'Error: {e}')
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, nama, kelas, nis FROM siswa WHERE is_active = true ORDER BY nama")
            siswa_data = cursor.fetchall()
        siswa_list = [{'id': s[0], 'nama': s[1], 'kelas': s[2], 'nis': s[3]} for s in siswa_data]
    except Exception as e:
        print(f"Error ambil siswa: {e}")
        siswa_list = []
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, judul, stok FROM buku WHERE stok > 0 ORDER BY judul")
            buku_data = cursor.fetchall()
        buku_list = [{'id': b[0], 'judul': b[1], 'stok': b[2]} for b in buku_data]
    except Exception as e:
        print(f"Error ambil buku: {e}")
        buku_list = []
    
    return render(request, 'peminjaman/create_peminjaman.html', {
        'siswa_list': siswa_list,
        'buku_list': buku_list,
        'today': today,
        'jatuh_tempo': jatuh_tempo_default
    })


def peminjaman_list(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT p.id, s.nama, s.kelas, b.judul, 
                       TO_CHAR(p.tanggal_pinjam, 'DD Mon YYYY') as tgl_pinjam,
                       TO_CHAR(p.jatuh_tempo, 'DD Mon YYYY') as tgl_tempo,
                       p.keperluan, p.status, p.catatan, p.petugas
                FROM peminjaman p
                JOIN siswa s ON p.siswa_id = s.id
                JOIN buku b ON p.buku_id = b.id
                ORDER BY p.id DESC
            """)
            peminjaman_data = cursor.fetchall()
        
        peminjaman_list_data = []
        for p in peminjaman_data:
            peminjaman_list_data.append({
                'id': p[0],
                'nama': p[1],
                'kelas': p[2],
                'judul': p[3],
                'tanggal_pinjam': p[4],
                'jatuh_tempo': p[5],
                'keperluan': p[6] if p[6] else '-',
                'status': p[7] if p[7] else 'Dipinjam',
                'catatan': p[8] if len(p) > 8 and p[8] else '',
                'petugas': p[9] if len(p) > 9 and p[9] else 'Budi Siregar'
            })
        
    except Exception as e:
        print(f"Error peminjaman_list: {e}")
        peminjaman_list_data = []
    
    return render(request, 'peminjaman/list_peminjaman.html', {'peminjaman': peminjaman_list_data})


# === INI FUNGSI BARU YANG TADI HILANG ===
def peminjaman_return(request, id):
    try:
        with connection.cursor() as cursor:
            # 1. Ambil data buku_id dulu dari tabel peminjaman
            cursor.execute("SELECT buku_id FROM peminjaman WHERE id = %s", [id])
            result = cursor.fetchone()
            
            if result:
                buku_id = result[0]
                # 2. Update status peminjaman jadi Dikembalikan
                cursor.execute("UPDATE peminjaman SET status = 'Dikembalikan' WHERE id = %s", [id])
                # 3. Kembalikan jumlah stok buku (+1)
                cursor.execute("UPDATE buku SET stok = stok + 1 WHERE id = %s", [buku_id])
                
                messages.success(request, 'Buku berhasil dikembalikan!')
            else:
                messages.error(request, 'Data peminjaman tidak ditemukan!')
                
    except Exception as e:
        print(f"Error peminjaman_return: {e}")
        messages.error(request, f'Gagal mengembalikan buku: {e}')
        
    return redirect('peminjaman_list')