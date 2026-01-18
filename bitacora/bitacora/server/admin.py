from django.contrib import admin
from .models import *

@admin.register(Ubicacion)
class UbicacionAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

@admin.register(Responsable)
class ResponsableAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

class BitacoraAccesoAdmin(admin.ModelAdmin):
    list_display = ('id','get_codigo', 'fecha', 'hora_entrada', 'hora_salida', 'nombre_visitante', 'ubicacion',  'responsable','externo')
    list_filter = ('fecha', 'ubicacion', 'responsable')
    search_fields = ('nombre_visitante', 'rut', 'ticket')
    ordering = ('-fecha', '-hora_entrada')
    fieldsets = (
        (None, {
            'fields': ('fecha', 'hora_entrada', 'hora_salida', 'nombre_visitante', 'ubicacion', 'responsable')
        }),
        ('Detalles adicionales', {
            'fields': ('observaciones', 'rut', 'apellido_paterno', 'apellido_materno', 'ticket'),
        }),
    )

    @admin.display(description="Código")
    def get_codigo(self, obj):
        return f"BA-{obj.id:06d}" 

admin.site.register(BitacoraAcceso, BitacoraAccesoAdmin)

