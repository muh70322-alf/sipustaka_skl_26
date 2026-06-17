from django.urls import path
from . import views

urlpatterns = [
    path('', views.peminjaman_list, name='peminjaman_list'),
    path('tambah/', views.peminjaman_create, name='peminjaman_create'),
    path('kembalikan/<int:id>/', views.peminjaman_return, name='peminjaman_return'),
]