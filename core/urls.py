# core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Rutas existentes:
    path('', views.dashboard, name='dashboard'), 
    
    # 📌 LAS NUEVAS RUTAS DEBEN ESTAR AQUÍ:
    path('docente/asistencia/', views.lista_asistencia_docente, name='lista_asistencia'),
    path('docente/asistencia/editar/<int:estudiante_id>/', views.editar_asistencia_docente, name='editar_asistencia'),
]