from django.urls import path
from . import views

urlpatterns = [
    path('', views.siswa_list, name='siswa_list'),
    path('tambah/', views.siswa_create, name='siswa_create'),
    path('detail/<int:id>/', views.siswa_detail, name='siswa_detail'),
    path('edit/<int:id>/', views.siswa_edit, name='siswa_edit'),
    path('hapus/<int:id>/', views.siswa_delete_confirm, name='siswa_delete_confirm'),
    path('delete/<int:id>/', views.siswa_delete, name='siswa_delete'),
]