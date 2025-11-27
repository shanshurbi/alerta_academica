from django.db import models

class Estudiante(models.Model):
    nombre = models.CharField(max_length=100)
    promedio = models.FloatField()
    asistencia = models.FloatField()  # Se asume que es un valor entre 0.0 y 1.0
    tareas_entregadas = models.IntegerField()

    def __str__(self):
        return self.nombre

class Alerta(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    riesgo = models.FloatField()  # Predicción entre 0 y 1
    mensaje = models.CharField(max_length=255)
    fecha = models.DateTimeField(auto_now_add=True) # auto_now_add cumple el requisito de guardar la fecha

    def __str__(self):
        return f"Alerta para {self.estudiante.nombre} - Riesgo: {self.riesgo:.2f}"
