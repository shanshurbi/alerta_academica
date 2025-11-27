# core/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Estudiante, Alerta
from .modelo_ia import predecir_riesgo # <-- ¡CORRECCIÓN A modelo_ia!

# 1. Función para mostrar el Dashboard (Ruta: /)
def dashboard(request):
    """
    Muestra la lista de estudiantes y sus alertas recientes.
    """
    # Recupera todos los estudiantes
    estudiantes = Estudiante.objects.all().order_by('nombre')
    
    # Prepara los datos para el template (opcional: buscar la última alerta)
    estudiantes_data = []
    for estudiante in estudiantes:
        ultima_alerta = Alerta.objects.filter(estudiante=estudiante).order_by('-fecha').first()
        estudiantes_data.append({
            'estudiante': estudiante,
            'ultima_alerta': ultima_alerta
        })
        
    context = {
        'estudiantes_data': estudiantes_data,
        'titulo': 'Dashboard de Riesgo Académico'
    }
    # Renderiza el dashboard.html
    return render(request, 'dashboard.html', context)


# 2. Función para Generar la Alerta (Ruta: /alerta/<id>/)
def generar_alerta(request, estudiante_id):
    """
    Recupera los datos del estudiante, los pasa al modelo IA, 
    guarda la nueva Alerta y redirige al dashboard.
    """
    # 1. Recuperar estudiante o devolver 404
    estudiante = get_object_or_404(Estudiante, pk=estudiante_id)

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

    # 4. Guardar la nueva alerta en la DB (requisito cumplido)
    Alerta.objects.create(
        estudiante=estudiante,
        riesgo=riesgo,
        mensaje=mensaje
    )

    # 5. Redirigir al dashboard para ver el resultado
    return redirect('dashboard')