# core/ia_modelo.py

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from joblib import dump, load # Usamos joblib para serializar el modelo

# Nombre del archivo donde se guardará el modelo entrenado
MODEL_PATH = 'core/modelo_riesgo.joblib'

def entrenar_modelo_simulado():
    """
    Genera datos sintéticos, entrena un RandomForestClassifier y lo guarda.
    Esto simula un entrenamiento inicial en un entorno real.
    """
    print("-> Generando datos simulados y entrenando el modelo...")
    
    # 1. GENERACIÓN DE DATOS SIMULADOS
    N = 100 # 100 estudiantes simulados
    
    # Simulación de métricas:
    # Promedio (entre 3.0 y 5.0)
    promedio = np.random.uniform(3.0, 5.0, N)
    # Asistencia (entre 0.6 y 1.0)
    asistencia = np.random.uniform(0.6, 1.0, N)
    # Tareas Entregadas (entre 5 y 15)
    tareas = np.random.randint(5, 16, N)
    
    # 2. CREACIÓN DE LA VARIABLE OBJETIVO (RIESGO SIMULADO)
    # El riesgo binario (1 = Riesgo, 0 = No Riesgo) se define
    # basado en una simple regla simulada: bajo promedio O baja asistencia.
    riesgo_binario = np.where((promedio < 3.5) | (asistencia < 0.7), 1, 0)
    
    data = pd.DataFrame({
        'promedio': promedio,
        'asistencia': asistencia,
        'tareas_entregadas': tareas,
        'riesgo': riesgo_binario
    })
    
    X = data[['promedio', 'asistencia', 'tareas_entregadas']]
    y = data['riesgo']
    
    # 3. ENTRENAMIENTO DEL MODELO OBLIGATORIO (RandomForestClassifier)
    model = RandomForestClassifier(random_state=42)
    model.fit(X, y)
    
    # 4. SERIALIZACIÓN (Guardar el modelo)
    dump(model, MODEL_PATH)
    print(f"-> Modelo entrenado y guardado en: {MODEL_PATH}")


def predecir_riesgo(promedio: float, asistencia: float, tareas: int) -> float:
    """
    Carga el modelo serializado y predice el riesgo (probabilidad entre 0 y 1)
    para un estudiante específico.
    """
    try:
        # 1. Cargar el modelo guardado
        model = load(MODEL_PATH)
    except FileNotFoundError:
        print("¡Advertencia! Modelo no encontrado. Entrenando modelo de respaldo...")
        entrenar_modelo_simulado()
        model = load(MODEL_PATH)
    
    # 2. Preparar los datos de entrada para la predicción (como un DataFrame)
    # El modelo espera un array 2D
    input_data = pd.DataFrame([[promedio, asistencia, tareas]], 
                              columns=['promedio', 'asistencia', 'tareas_entregadas'])
    
    # 3. Realizar la predicción de probabilidad (Probabilidad de clase 1 = Riesgo)
    # [0] es para la primera (y única) muestra, [1] es la probabilidad de la clase 'riesgo' (1)
    riesgo_probabilidad = model.predict_proba(input_data)[0][1]
    
    # 4. Retornar el valor entre 0 y 1 (requisito cumplido)
    return riesgo_probabilidad

# Para asegurar que el modelo se cree al iniciar el proyecto por primera vez
if __name__ == '__main__':
    entrenar_modelo_simulado()