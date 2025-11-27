# 📌 PROTOTIPO: SISTEMA DE ALERTA DE RIESGO ACADÉMICO (Django + IA)

## 🎯 Objetivo del Proyecto
Prototipo funcional desarrollado como entregable académico/profesional, cuyo objetivo es demostrar la capacidad de generar alertas tempranas de riesgo académico en estudiantes basándose en sus métricas de desempeño.

## 🚀 Tecnologías Utilizadas
* **Backend:** Django (v5.x)
* **Base de Datos:** SQLite
* **Inteligencia Artificial (IA):** scikit-learn, pandas, numpy
* **Control de Versiones:** Git y GitHub

## ⚙️ Estructura del Proyecto
* **alerta_ia:** Proyecto principal.
* **core:** Aplicación Django que contiene modelos, vistas y lógica de IA.
* **core/ia_modelo.py:** Script que entrena y serializa un `RandomForestClassifier` con datos simulados para calcular el riesgo (valor entre 0 y 1).

## 📝 Instrucciones de Instalación y Ejecución

### 1. Clonar el Repositorio
```bash
git clone [https://docs.github.com/es/repositories/creating-and-managing-repositories/quickstart-for-repositories](https://docs.github.com/es/repositories/creating-and-managing-repositories/quickstart-for-repositories)
cd alerta_ia_root