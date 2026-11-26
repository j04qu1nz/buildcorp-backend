import re

from django.utils import timezone
from rest_framework import serializers

from .models import Alquiler, Contratista, Herramienta, Mantenimiento


class ContratistaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contratista
        fields = '__all__'

    def validate_telefono(self, value):
        if not re.fullmatch(r'\+?\d{8,15}', value):
            raise serializers.ValidationError('El teléfono debe tener entre 8 y 15 dígitos (puede iniciar con +).')
        return value


class HerramientaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Herramienta
        fields = '__all__'
        extra_kwargs = {
            'horas_uso_acumuladas': {'min_value': 0},
            'limite_horas_mantenimiento': {'min_value': 1},
        }


class AlquilerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alquiler
        fields = '__all__'
        read_only_fields = ('fecha_salida',)

    def validate(self, data):
        # Reglas de negocio: se devuelven como 400 (y no como error 500 del modelo)
        if self.instance is None:
            if data['contratista'].bloqueado:
                raise serializers.ValidationError(
                    {'contratista': 'El contratista está bloqueado por morosidad.'})
            if data['herramienta'].estado in ('Mantenimiento', 'Dado de Baja'):
                raise serializers.ValidationError(
                    {'herramienta': 'La herramienta no está disponible para alquiler.'})
            if data['fecha_devolucion_estimada'] <= timezone.now():
                raise serializers.ValidationError(
                    {'fecha_devolucion_estimada': 'La fecha de devolución estimada debe ser futura.'})
        return data


class MantenimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mantenimiento
        fields = '__all__'

    def validate_fecha_programada(self, value):
        if self.instance is None and value < timezone.localdate():
            raise serializers.ValidationError('La fecha programada no puede estar en el pasado.')
        return value