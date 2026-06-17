from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import connection
from django.db import IntegrityError

def list_buku(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, judul, pengarang, kategori, penerbit, tahun_terbit, rak, stok 
                FROM buku 
                ORDER BY id
            """)
            books = cursor.fetchall()
        
        books_list = []
        for book in books:
            books_list.append({
                'id': book[0],
                'judul': book[1],
                'pengarang': book[2],
                'kategori': book[3],
                'penerbit': book[4],
                'tahun_terbit': book[5],
                'rak': book[6],
                'stok': book[7],
            })
    except Exception as e:
        print(f"Error: {e}")
        books_list = []
        messages.error(request, f'Error mengambil data: {e}')
    
    return render(request, 'buku/list_buku.html', {'books': books_list})

def tambah_buku(request):
    if request.method == 'POST':
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO buku (judul, pengarang, kategori, penerbit, tahun_terbit, rak, stok, deskripsi)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, [
                    request.POST.get('judul'),
                    request.POST.get('pengarang'),
                    request.POST.get('kategori'),
                    request.POST.get('penerbit'),
                    request.POST.get('tahun_terbit'),
                    request.POST.get('rak'),
                    request.POST.get('stok'),
                    request.POST.get('deskripsi', '')
                ])
            messages.success(request, 'Buku berhasil ditambahkan!')
            return redirect('list_buku')
        except Exception as e:
            messages.error(request, f'Error: {e}')
    
    return render(request, 'buku/tambah_buku.html')

def detail_buku(request, id):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM buku WHERE id = %s", [id])
            book = cursor.fetchone()
        
        if book:
            book_detail = {
                'id': book[0],
                'judul': book[1],
                'pengarang': book[2],
                'kategori': book[3],
                'penerbit': book[4],
                'tahun_terbit': book[5],
                'rak': book[6],
                'stok': book[7],
                'deskripsi': book[8] if len(book) > 8 else ''
            }
            return render(request, 'buku/detail_buku.html', {'book': book_detail})
        else:
            messages.error(request, 'Buku tidak ditemukan!')
            return redirect('list_buku')
    except Exception as e:
        messages.error(request, f'Error: {e}')
        return redirect('list_buku')

def edit_buku(request, id):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM buku WHERE id = %s", [id])
            book = cursor.fetchone()
        
        if not book:
            messages.error(request, 'Buku tidak ditemukan!')
            return redirect('list_buku')
        
        if request.method == 'POST':
            cursor.execute("""
                UPDATE buku SET 
                    judul = %s,
                    pengarang = %s,
                    kategori = %s,
                    penerbit = %s,
                    tahun_terbit = %s,
                    rak = %s,
                    stok = %s,
                    deskripsi = %s
                WHERE id = %s
            """, [
                request.POST.get('judul'),
                request.POST.get('pengarang'),
                request.POST.get('kategori'),
                request.POST.get('penerbit'),
                request.POST.get('tahun_terbit'),
                request.POST.get('rak'),
                request.POST.get('stok'),
                request.POST.get('deskripsi', ''),
                id
            ])
            messages.success(request, 'Buku berhasil diupdate!')
            return redirect('list_buku')
        
        book_detail = {
            'id': book[0],
            'judul': book[1],
            'pengarang': book[2],
            'kategori': book[3],
            'penerbit': book[4],
            'tahun_terbit': book[5],
            'rak': book[6],
            'stok': book[7],
            'deskripsi': book[8] if len(book) > 8 else ''
        }
        return render(request, 'buku/edit_buku.html', {'book': book_detail})
        
    except Exception as e:
        messages.error(request, f'Error: {e}')
        return redirect('list_buku')

def hapus_buku_confirm(request, id):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, judul, stok FROM buku WHERE id = %s", [id])
            book = cursor.fetchone()
        
        if not book:
            messages.error(request, 'Buku tidak ditemukan!')
            return redirect('list_buku')
        
        book_detail = {
            'id': book[0],
            'judul': book[1],
            'stok': book[2]
        }
        return render(request, 'buku/hapus_buku.html', {'book': book_detail})
    except Exception as e:
        messages.error(request, f'Error: {e}')
        return redirect('list_buku')

def hapus_buku_proses(request, id):
    try:
        with connection.cursor() as cursor:
            # Cek apakah buku ada
            cursor.execute("SELECT judul FROM buku WHERE id = %s", [id])
            book = cursor.fetchone()
            
            if book:
                cursor.execute("DELETE FROM buku WHERE id = %s", [id])
                messages.success(request, f'Buku "{book[0]}" berhasil dihapus!')
            else:
                messages.error(request, 'Buku tidak ditemukan!')
    except Exception as e:
        messages.error(request, f'Error: {e}')
    
    return redirect('list_buku')