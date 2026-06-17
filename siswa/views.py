from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import connection

def siswa_list(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, nama, kelas, nis, is_active FROM siswa ORDER BY id")
            siswa_data = cursor.fetchall()
        
        siswa_list = []
        for s in siswa_data:
            siswa_list.append({
                'id': s[0],
                'nama': s[1],
                'kelas': s[2],
                'nis': s[3],
                'is_active': s[4]
            })
    except Exception as e:
        print(f"Error siswa_list: {e}")
        siswa_list = []
    
    return render(request, 'siswa/list_siswa.html', {'siswa': siswa_list})

def siswa_detail(request, id):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, nama, kelas, nis, is_active FROM siswa WHERE id = %s", [id])
            siswa_data = cursor.fetchone()
            
            if not siswa_data:
                messages.error(request, 'User tidak ditemukan!')
                return redirect('siswa_list')
            
            # Hitung total peminjaman
            cursor.execute("SELECT COUNT(*) FROM peminjaman WHERE siswa_id = %s", [id])
            total_peminjaman = cursor.fetchone()[0] or 0
            
            # Hitung peminjaman aktif
            cursor.execute("SELECT COUNT(*) FROM peminjaman WHERE siswa_id = %s AND status = 'Dipinjam'", [id])
            peminjaman_aktif = cursor.fetchone()[0] or 0
        
        siswa_detail = {
            'id': siswa_data[0],
            'nama': siswa_data[1],
            'kelas': siswa_data[2],
            'nis': siswa_data[3],
            'is_active': siswa_data[4]
        }
        
        return render(request, 'siswa/detail_siswa.html', {
            'siswa': siswa_detail,
            'total_peminjaman': total_peminjaman,
            'peminjaman_aktif': peminjaman_aktif
        })
    except Exception as e:
        messages.error(request, f'Error: {e}')
        return redirect('siswa_list')

def siswa_edit(request, id):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, nama, kelas, nis, is_active FROM siswa WHERE id = %s", [id])
            siswa_data = cursor.fetchone()
        
        if not siswa_data:
            messages.error(request, 'User tidak ditemukan!')
            return redirect('siswa_list')
        
        if request.method == 'POST':
            nama = request.POST.get('nama')
            kelas = request.POST.get('kelas')
            nis = request.POST.get('nis')
            is_active = request.POST.get('is_active', '1')
            
            cursor.execute("""
                UPDATE siswa SET nama=%s, kelas=%s, nis=%s, is_active=%s
                WHERE id=%s
            """, [nama, kelas, nis, is_active, id])
            messages.success(request, f'User {nama} berhasil diupdate!')
            return redirect('siswa_list')
        
        siswa_detail = {
            'id': siswa_data[0],
            'nama': siswa_data[1],
            'kelas': siswa_data[2],
            'nis': siswa_data[3],
            'is_active': siswa_data[4]
        }
        return render(request, 'siswa/edit_siswa.html', {'siswa': siswa_detail})
    except Exception as e:
        messages.error(request, f'Error: {e}')
        return redirect('siswa_list')

def siswa_delete_confirm(request, id):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, nama, nis, kelas FROM siswa WHERE id = %s", [id])
            siswa_data = cursor.fetchone()
        
        if not siswa_data:
            messages.error(request, 'User tidak ditemukan!')
            return redirect('siswa_list')
        
        siswa_detail = {
            'id': siswa_data[0],
            'nama': siswa_data[1],
            'nis': siswa_data[2],
            'kelas': siswa_data[3]
        }
        return render(request, 'siswa/hapus_siswa.html', {'siswa': siswa_detail})
    except Exception as e:
        messages.error(request, f'Error: {e}')
        return redirect('siswa_list')

def siswa_delete(request, id):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT nama FROM siswa WHERE id = %s", [id])
            siswa = cursor.fetchone()
            
            if siswa:
                cursor.execute("DELETE FROM siswa WHERE id = %s", [id])
                messages.success(request, f'User {siswa[0]} berhasil dihapus!')
            else:
                messages.error(request, 'User tidak ditemukan!')
    except Exception as e:
        messages.error(request, f'Error: {e}')
    
    return redirect('siswa_list')

def siswa_create(request):
    if request.method == 'POST':
        nama = request.POST.get('nama')
        kelas = request.POST.get('kelas')
        nis = request.POST.get('nis')
        is_active = request.POST.get('is_active', '1')
        
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id FROM siswa WHERE nis = %s", [nis])
                existing = cursor.fetchone()
                
                if existing:
                    messages.error(request, f'NIS {nis} sudah terdaftar!')
                else:
                    cursor.execute("""
                        INSERT INTO siswa (nama, kelas, nis, is_active)
                        VALUES (%s, %s, %s, %s)
                    """, [nama, kelas, nis, is_active])
                    messages.success(request, f'User {nama} berhasil ditambahkan!')
                    return redirect('siswa_list')
        except Exception as e:
            messages.error(request, f'Error: {e}')
    
    return render(request, 'siswa/tambah_siswa.html')