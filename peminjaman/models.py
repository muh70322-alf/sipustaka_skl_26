from django.db import models
from buku.models import Buku
from siswa.models import Siswa

class Peminjaman(models.Model):
    STATUS_CHOICES = [
        ('Dipinjam', 'Dipinjam'),
        ('Dikembalikan', 'Dikembalikan'),
        ('Terlambat', 'Terlambat'),
    ]
    
    siswa = models.ForeignKey(Siswa, on_delete=models.CASCADE)
    buku = models.ForeignKey(Buku, on_delete=models.CASCADE)
    tanggal_pinjam = models.DateField()
    jatuh_tempo = models.DateField()
    keperluan = models.TextField()
    catatan = models.TextField(blank=True, null=True)
    petugas = models.CharField(max_length=100, default='Budi Siregar')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Dipinjam')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'peminjaman'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.siswa.nama} - {self.buku.judul}"