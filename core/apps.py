# core/apps.py

from django.apps import AppConfig

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    
    # 📌 ¡LA CLAVE: Sobreescribir el método ready!
    def ready(self):
        import core.signals # Carga el módulo de señales al inicio