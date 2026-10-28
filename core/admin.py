from django.contrib import admin
from .models import Contratista, Herramienta, Alquiler, Mantenimiento

@admin.register(Contratista)
class ContratistaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'empresa', 'rut', 'telefono', 'es_moroso', 'bloqueado')
    list_filter = ('es_moroso', 'bloqueado', 'empresa')
    search_fields = ('nombre', 'rut', 'empresa')
    list_editable = ('es_moroso', 'bloqueado')

@admin.register(Herramienta)
class HerramientaAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'categoria', 'estado', 'horas_uso_acumuladas', 'limite_horas_mantenimiento')
    list_filter = ('estado', 'categoria')
    search_fields = ('codigo', 'nombre')
    list_editable = ('estado', 'horas_uso_acumuladas')

@admin.register(Alquiler)
class AlquilerAdmin(admin.ModelAdmin):
    list_display = ('id', 'herramienta', 'contratista', 'fecha_salida', 'fecha_devolucion_estimada', 'devuelto')
    list_filter = ('devuelto', 'fecha_salida')
    search_fields = ('herramienta__nombre', 'contratista__nombre', 'contratista__rut')

@admin.register(Mantenimiento)
class MantenimientoAdmin(admin.ModelAdmin):
    list_display = ('herramienta', 'fecha_programada', 'realizado')
    list_filter = ('realizado', 'fecha_programada')
    search_fields = ('herramienta__nombre', 'descripcion')
    list_editable = ('realizado',)