# core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Ruta raíz de la app (mapeada a /)
    path('', views.dashboard, name='dashboard'), 
    # Endpoint para generar la alerta: /alerta/<id>/
    path('alerta/<int:estudiante_id>/', views.generar_alerta, name='generar_alerta'),
]