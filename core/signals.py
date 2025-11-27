# core/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Estudiante, Alerta
from .modelo_ia import predecir_riesgo # Usamos tu modelo_ia.py

@receiver(post_save, sender=Estudiante)
def generar_alerta_automatica(sender, instance, created, **kwargs):
    """
    Señal que se dispara después de que un objeto Estudiante es guardado (creado o modificado).
    """
    # 1. Recuperar la instancia del Estudiante (instance es el objeto Estudiante recién guardado)
    estudiante = instance

    # 2. Llamar al modelo de IA
    riesgo = predecir_riesgo(
        promedio=estudiante.promedio,
        asistencia=estudiante.asistencia,
        tareas=estudiante.tareas_entregadas
    )

    # 3. Determinar el mensaje basado en el riesgo
    if riesgo >= 0.75:
        mensaje = "Riesgo Alto: Requiere intervención inmediata."
    elif riesgo >= 0.4:
        mensaje = "Riesgo Medio: Monitoreo recomendado."
    else:
        mensaje = "Riesgo Bajo: Desempeño satisfactorio."

    # 4. Guardar la nueva alerta en la DB (se creará una nueva alerta con la fecha actual)
    Alerta.objects.create(
        estudiante=estudiante,
        riesgo=riesgo,
        mensaje=mensaje
    )
    
    # OPCIONAL: Para evitar generar demasiadas alertas en el futuro,
    # podríamos añadir lógica para solo generar alertas si el riesgo es alto
    # o si el riesgo cambió significativamente desde la última alerta.
    print(f"Alerta automática generada para {estudiante.nombre}. Riesgo: {riesgo:.3f}")