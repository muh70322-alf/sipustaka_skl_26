from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_buku, name='list_buku'),
    path('tambah/', views.tambah_buku, name='tambah_buku'),
    path('detail/<int:id>/', views.detail_buku, name='detail_buku'),
    path('edit/<int:id>/', views.edit_buku, name='edit_buku'),
    path('hapus/<int:id>/', views.hapus_buku_confirm, name='hapus_buku_confirm'),
    path('hapus-proses/<int:id>/', views.hapus_buku_proses, name='hapus_buku_proses'),
]