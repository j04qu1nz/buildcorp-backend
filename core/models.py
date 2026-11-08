from django.db import models

class Contratista(models.Model):
    nombre = models.CharField(max_length=150)
    empresa = models.CharField(max_length=150)
    rut = models.CharField(max_length=20, unique=True)
    telefono = models.CharField(max_length=25)
    es_moroso = models.BooleanField(default=False)
    bloqueado = models.BooleanField(default=False, help_text="Bloqueo automático por morosidad")

    def __str__(self):
        return f"{self.nombre} ({self.empresa}) - Bloqueado: {self.bloqueado}"


class Herramienta(models.Model):
    ESTADOS = [
        ('Disponible', 'Disponible'),
        ('En Uso', 'En Uso'),
        ('Mantenimiento', 'Mantenimiento'),
        ('Dado de Baja', 'Dado de Baja'),
    ]
    codigo = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=100)
    categoria = models.CharField(max_length=100)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='Disponible')
    horas_uso_acumuladas = models.IntegerField(default=0)
    limite_horas_mantenimiento = models.IntegerField(default=100)

    def __str__(self):
        return f"[{self.codigo}] {self.nombre} - Estado: {self.estado}"


class Alquiler(models.Model):
    herramienta = models.ForeignKey(Herramienta, on_delete=models.CASCADE)
    contratista = models.ForeignKey(Contratista, on_delete=models.CASCADE)
    fecha_salida = models.DateTimeField(auto_now_add=True)
    fecha_devolucion_estimada = models.DateTimeField()
    fecha_devolucion_real = models.DateTimeField(null=True, blank=True)
    firma_digital = models.TextField(help_text="Texto o representación de la firma digital del responsable de obra")
    devuelto = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.contratista.bloqueado:
            raise ValueError("No se puede realizar el alquiler: El contratista está bloqueado por morosidad.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Alquiler #{self.id} | {self.herramienta.nombre} a {self.contratista.nombre}"


class Mantenimiento(models.Model):
    herramienta = models.ForeignKey(Herramienta, on_delete=models.CASCADE)
    fecha_programada = models.DateField()
    descripcion = models.TextField()
    realizado = models.BooleanField(default=False)

    def __str__(self):
        return f"Mantenimiento para {self.herramienta.nombre} el {self.fecha_programada}"