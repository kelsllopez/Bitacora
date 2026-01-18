from django.contrib import admin
from .models import BitacoraInterna, BitacoraExterna

@admin.register(BitacoraInterna)
class BitacoraInternaAdmin(admin.ModelAdmin):
    list_display = ['fecha', 'hora_entrada', 'nombre_visitante', 'apellido_paterno', 
                    'rut', 'modo_visita', 'responsable', 'ubicacion']
    list_filter = ['fecha', 'modo_visita', 'ubicacion']
    search_fields = ['nombre_visitante', 'apellido_paterno', 'apellido_materno', 
                     'rut', 'responsable', 'ubicacion']
    date_hierarchy = 'fecha'
    ordering = ['-fecha', '-hora_entrada']
    
    fieldsets = (
        ('Información de Fecha y Hora', {
            'fields': ('fecha', 'hora_entrada', 'hora_salida')
        }),
        ('Información del Visitante', {
            'fields': ('nombre_visitante', 'apellido_paterno', 'apellido_materno', 'rut')
        }),
        ('Detalles de la Visita', {
            'fields': ('modo_visita', 'ticket', 'responsable', 'ubicacion', 'observaciones')
        }),
        ('Información del Sistema', {
            'fields': ('creado_por',),
            'classes': ('collapse',)
        })
    )

@admin.register(BitacoraExterna)
class BitacoraExternaAdmin(admin.ModelAdmin):
    list_display = ['fecha', 'hora_entrada', 'nombre_visitante', 'modo_visita', 
                    'responsable', 'ubicacion']
    list_filter = ['fecha', 'modo_visita', 'ubicacion']
    search_fields = ['nombre_visitante', 'responsable', 'ubicacion']
    date_hierarchy = 'fecha'
    ordering = ['-fecha', '-hora_entrada']
    
    fieldsets = (
        ('Información de Fecha y Hora', {
            'fields': ('fecha', 'hora_entrada', 'hora_salida')
        }),
        ('Información del Visitante', {
            'fields': ('nombre_visitante',)
        }),
        ('Detalles de la Visita', {
            'fields': ('modo_visita', 'ticket', 'responsable', 'ubicacion', 'observaciones')
        }),
        ('Información del Sistema', {
            'fields': ('creado_por',),
            'classes': ('collapse',)
        })
    )