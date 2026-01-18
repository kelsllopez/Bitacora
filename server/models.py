from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class BitacoraInterna(models.Model):
    UBICACION_CHOICES = [
        ('sala_servidores', 'Sala de Servidores'),
        ('sala_comunicaciones', 'Sala de comunicaciones'),
    ]
    
    RESPONSABLE__BITACORA = [
        ('jefe_informatica', 'Jefe de  Informatica'),
    ]
    fecha = models.DateField(default=timezone.now)
    hora_entrada = models.TimeField()
    hora_salida = models.TimeField(null=True, blank=True)
    modo_visita = models.TextField(blank=True, null=True)
    nombre_visitante = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=100)
    apellido_materno = models.CharField(max_length=100)
    rut = models.CharField(max_length=12)
    ticket = models.CharField(max_length=50, blank=True, null=True)
    responsable = models.CharField(max_length=20, choices=RESPONSABLE__BITACORA)
    ubicacion = models.CharField(max_length=20, choices=UBICACION_CHOICES)
    observaciones = models.TextField(blank=True, null=True)
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-fecha', '-hora_entrada']
        verbose_name = 'Bitácora Interna'
        verbose_name_plural = 'Bitácoras Internas'
    
    def __str__(self):
        return f"{self.nombre_visitante} {self.apellido_paterno} - {self.fecha}"

class BitacoraExterna(models.Model):
    UBICACION_CHOICES = [
        ('sala_servidores', 'Sala de Servidores'),
        ('sala_comunicaciones', 'Sala de comunicaciones'),

    ]
    RESPONSABLE__BITACORA = [
        ('jefe_informatica', 'Jefe de  Informatica'),
    ]
    fecha = models.DateField(default=timezone.now)
    hora_entrada = models.TimeField()
    hora_salida = models.TimeField(null=True, blank=True)
    modo_visita = models.TextField(blank=True, null=True)
    nombre_visitante = models.CharField(max_length=100)
    ticket = models.CharField(max_length=50, blank=True, null=True)
    responsable = models.CharField(max_length=20, choices=RESPONSABLE__BITACORA)
    ubicacion = models.CharField(max_length=20, choices=UBICACION_CHOICES)
    observaciones = models.TextField(blank=True, null=True)
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-fecha', '-hora_entrada']
        verbose_name = 'Bitácora Externa'
        verbose_name_plural = 'Bitácoras Externas'
    
    def __str__(self):
        return f"{self.nombre_visitante} - {self.fecha}"