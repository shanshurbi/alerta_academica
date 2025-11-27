# core/admin.py
from django.contrib import admin
from .models import Estudiante, Alerta

# 1. Definir cómo se verá el modelo Estudiante
class EstudianteAdmin(admin.ModelAdmin):
    # Campos que se mostrarán en la lista de Estudiantes
    list_display = ('nombre', 'promedio', 'asistencia', 'tareas_entregadas')

# 2. Definir cómo se verá el modelo Alerta
class AlertaAdmin(admin.ModelAdmin):
    # Campos que se mostrarán en la lista de Alertas
    list_display = ('estudiante', 'riesgo', 'mensaje', 'fecha') # <-- ¡AQUÍ ESTÁ LA CLAVE!
    # Permite filtrar por estudiante
    list_filter = ('estudiante',) 
    # Permite buscar alertas por mensaje
    search_fields = ('mensaje',) 

# 3. Registrar los modelos con sus clases de personalización
admin.site.register(Estudiante, EstudianteAdmin)
admin.site.register(Alerta, AlertaAdmin)