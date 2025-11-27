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

# Nueva Vista 1: Lista de Asistencia (Ruta: /docente/asistencia/)
def lista_asistencia_docente(request):
    """
    Muestra la lista de estudiantes con sus asistencias actuales
    para que el docente pueda editar.
    """
    estudiantes = Estudiante.objects.all().order_by('nombre')
    context = {
        'estudiantes': estudiantes,
        'titulo': 'Panel de Asistencia del Docente'
    }
    return render(request, 'docente_asistencia.html', context)


# Nueva Vista 2: Edición de Asistencia (Ruta: /docente/asistencia/editar/<id>/)
def editar_asistencia_docente(request, estudiante_id):
    """
    Permite al docente editar la asistencia de un estudiante específico.
    """
    estudiante = get_object_or_404(Estudiante, pk=estudiante_id)

    if request.method == 'POST':
        # La asistencia viene del formulario como texto (request.POST['asistencia'])
        try:
            nueva_asistencia = float(request.POST['asistencia'])
            
            # Validación simple: debe estar entre 0.0 y 1.0
            if 0.0 <= nueva_asistencia <= 1.0:
                estudiante.asistencia = nueva_asistencia
                # Guardar el estudiante dispara la SIGNAL, generando la ALERTA automática.
                estudiante.save() 
                
                # Redirigir de vuelta a la lista para ver los cambios
                return redirect('lista_asistencia')
            else:
                # Si la validación falla, podemos manejar el error o simplemente recargar.
                pass 
        except ValueError:
             # Manejar si el input no es un número
             pass

    context = {
        'estudiante': estudiante,
        'titulo': f"Editar Asistencia de {estudiante.nombre}"
    }
    return render(request, 'docente_editar_asistencia.html', context)