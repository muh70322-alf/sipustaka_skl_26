from django import forms
from .models import Buku

class BukuForm(forms.ModelForm):
    class Meta:
        model = Buku
        fields = ['judul', 'pengarang', 'kategori', 'penerbit', 'tahun_terbit', 'rak', 'stok', 'deskripsi']
        widgets = {
            'judul': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan judul buku'}),
            'pengarang': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan nama pengarang'}),
            'kategori': forms.Select(attrs={'class': 'form-control'}),
            'penerbit': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan nama penerbit'}),
            'tahun_terbit': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Tahun terbit'}),
            'rak': forms.Select(attrs={'class': 'form-control'}),
            'stok': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Jumlah stok'}),
            'deskripsi': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Deskripsi buku'}),
        }