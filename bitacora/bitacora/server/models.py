from django.db import models
from django.db.models import Q
from django.utils import timezone
from datetime import datetime
from django.core.validators import RegexValidator
from simple_history.models import HistoricalRecords

class Ubicacion(models.Model):
    nombre = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.nombre


class Responsable(models.Model):
    nombre = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.nombre


class BitacoraAcceso(models.Model):
    fecha = models.DateField() 
    hora_entrada = models.TimeField(null=True, blank=True)
    hora_salida = models.TimeField(null=True, blank=True)

    nombre_visitante = models.CharField(max_length=255)
    ubicacion = models.ForeignKey(Ubicacion, on_delete=models.CASCADE)
    motivo_visita = models.TextField(blank=True, null=True) 
    responsable = models.ForeignKey(Responsable, on_delete=models.CASCADE)
    observaciones = models.TextField(blank=True, null=True)  # No obligatorio

    rut = models.CharField(max_length=15, blank=True, null=True)
    apellido_paterno = models.CharField(max_length=255, blank=True, null=True)
    apellido_materno = models.CharField(max_length=255, blank=True, null=True)
    ticket = models.CharField(max_length=255, blank=True, null=True)  # No obligatorio
    externo = models.BooleanField(default=False)  # Campo oculto
    history = HistoricalRecords()


    def save(self, *args, **kwargs):
        if self.hora_entrada:
            self.hora_entrada = timezone.make_naive(timezone.localtime(timezone.make_aware(datetime.combine(datetime.today(), self.hora_entrada))), timezone.get_current_timezone()).time()

        if self.hora_salida:
            self.hora_salida = timezone.make_naive(timezone.localtime(timezone.make_aware(datetime.combine(datetime.today(), self.hora_salida))), timezone.get_current_timezone()).time()

        super(BitacoraAcceso, self).save(*args, **kwargs)

    def __str__(self):
        return f"Bitacora Acceso - {self.nombre_visitante} - {self.fecha} - {self.id}"
    
    @property
    def tipo(self):
        return "Interna"  # Este modelo representa bitácoras internas
