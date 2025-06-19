from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class Usuario(models.Model):
    username = models.CharField(max_length=150, unique=True)
    correo = models.EmailField(unique=True)
    password = models.CharField(max_length=256)
    saldo = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.username

class TipoSeguro(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nombre

class SeguroContratado(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    tipo_seguro = models.ForeignKey(TipoSeguro, on_delete=models.CASCADE)
    fecha_contratacion = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.tipo_seguro.nombre}"

class Movimiento(models.Model):
    TIPOS = (
        ('DEPOSITO', 'Depósito'),
        ('RETIRO', 'Retiro'),
    )

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=TIPOS)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tipo} - {self.cantidad} - {self.usuario.username}"