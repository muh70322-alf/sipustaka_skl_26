from django.db import models

class Buku(models.Model):
    KATEGORI_CHOICES = [
        ('Novel', 'Novel'),
        ('Sejarah', 'Sejarah'),
        ('Pendidikan', 'Pendidikan'),
        ('Fiksi', 'Fiksi'),
        ('Fantasi', 'Fantasi'),
        ('Pengembangan Diri', 'Pengembangan Diri'),
        ('Autobiografi', 'Autobiografi'),
    ]
    
    RAK_CHOICES = [
        ('Rak A-01', 'Rak A-01'),
        ('Rak A-02', 'Rak A-02'),
        ('Rak A-03', 'Rak A-03'),
        ('Rak A-04', 'Rak A-04'),
        ('Rak A-05', 'Rak A-05'),
        ('Rak A1', 'Rak A1'),
        ('Rak A2', 'Rak A2'),
        ('Rak B1', 'Rak B1'),
        ('Rak B2', 'Rak B2'),
    ]
    
    judul = models.CharField(max_length=255)
    pengarang = models.CharField(max_length=255)
    kategori = models.CharField(max_length=50, choices=KATEGORI_CHOICES)
    penerbit = models.CharField(max_length=255)
    tahun_terbit = models.IntegerField(db_column='tahun_terbit')  # Sesuaikan dengan database
    rak = models.CharField(max_length=50)
    stok = models.IntegerField()
    deskripsi = models.TextField(blank=True, null=True)
    
    class Meta:
        db_table = 'buku'  # Nama tabel di database
        ordering = ['id']
    
    def __str__(self):
        return self.judul