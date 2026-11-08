from django.contrib import admin
from .models import Contratista, Herramienta, Alquiler, Mantenimiento

@admin.register(Contratista)
class ContratistaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'empresa', 'rut', 'telefono', 'es_moroso', 'bloqueado')
    list_filter = ('bloqueado', 'es_moroso')
    search_fields = ('nombre', 'empresa', 'rut')

    # Solo el Jefe (superusuario) puede crear, editar o eliminar contratistas y estados de morosidad
    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


@admin.register(Herramienta)
class HerramientaAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'categoria', 'estado', 'horas_uso_acumuladas', 'limite_horas_mantenimiento')
    list_filter = ('estado', 'categoria')
    search_fields = ('codigo', 'nombre', 'categoria')

    # Los trabajadores pueden ver las herramientas disponibles, pero no modificarlas ni crearlas
    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


@admin.register(Alquiler)
class AlquilerAdmin(admin.ModelAdmin):
    list_display = ('id', 'herramienta', 'contratista', 'fecha_salida', 'fecha_devolucion_estimada', 'devuelto')
    list_filter = ('devuelto', 'fecha_salida')
    search_fields = ('herramienta__nombre', 'contratista__nombre')

    # Tanto el jefe como los trabajadores pueden registrar nuevos alquileres/préstamos en terreno,
    # pero solo el jefe puede eliminarlos.
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


@admin.register(Mantenimiento)
class MantenimientoAdmin(admin.ModelAdmin):
    list_display = ('herramienta', 'fecha_programada', 'realizado')
    list_filter = ('realizado', 'fecha_programada')
    search_fields = ('herramienta__nombre',)

    # Restringido exclusivamente al Jefe
    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser