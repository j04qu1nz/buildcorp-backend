from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .models import Contratista, Herramienta, Alquiler, Mantenimiento
from .serializers import ContratistaSerializer, HerramientaSerializer, AlquilerSerializer, MantenimientoSerializer

class ContratistaViewSet(viewsets.ModelViewSet):
    queryset = Contratista.objects.all()
    serializer_class = ContratistaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['es_moroso', 'bloqueado']

class HerramientaViewSet(viewsets.ModelViewSet):
    queryset = Herramienta.objects.all()
    serializer_class = HerramientaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['estado', 'categoria']

class AlquilerViewSet(viewsets.ModelViewSet):
    queryset = Alquiler.objects.all()
    serializer_class = AlquilerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['devuelto', 'contratista']

class MantenimientoViewSet(viewsets.ModelViewSet):
    queryset = Mantenimiento.objects.all()
    serializer_class = MantenimientoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['realizado']