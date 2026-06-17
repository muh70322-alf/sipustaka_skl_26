from django.db import models

class Siswa(models.Model):
    nama = models.CharField(max_length=100)
    kelas = models.CharField(max_length=20)
    nis = models.CharField(max_length=20, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'siswa'
        ordering = ['nama']
    
    def __str__(self):
        return f"{self.nama} - {self.kelas}"