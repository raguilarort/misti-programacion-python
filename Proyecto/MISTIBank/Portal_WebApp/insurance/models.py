from django.db import models
from django.contrib.auth.models import User

class SeguroAuto(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=100)
    fecha_contratacion = models.DateField(auto_now_add=True)
    costo = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.usuario.username} - {self.tipo} ({self.fecha_contratacion})"
