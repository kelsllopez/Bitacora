# server/signals.py
import os
import json
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.serializers import serialize
from server.models import BitacoraAcceso

# Crear la carpeta "json" si no existe
if not os.path.exists('json'):
    os.makedirs('json')

# Respaldo automático con señales
@receiver(post_save, sender=BitacoraAcceso)
def backup_bitacora(sender, instance, created, **kwargs):
    if created:  # Solo cuando se crea un nuevo registro
        print("Nuevo registro creado, realizando respaldo automático.")
        # Obtener todos los registros de BitacoraAcceso
        bitacoras = BitacoraAcceso.objects.all()

        # Convertir todos los registros de BitacoraAcceso a formato JSON
        bitacoras_json = serialize('json', bitacoras)

        # Guardar los datos en un archivo JSON dentro de la carpeta "json"
        with open('json/respaldo_bitacora_automatico.json', 'w', encoding='utf-8') as json_file:
            json.dump(bitacoras_json, json_file, ensure_ascii=False, indent=4)
        print("Respaldo automático realizado con éxito.")
