from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from .models import Alquiler, Contratista, Herramienta, Mantenimiento
from .permissions import JefeOSoloLectura, SoloJefeElimina
from .serializers import (AlquilerSerializer, ContratistaSerializer,
                          HerramientaSerializer, MantenimientoSerializer)


class ContratistaViewSet(viewsets.ModelViewSet):
    queryset = Contratista.objects.all()
    serializer_class = ContratistaSerializer
    permission_classes = [JefeOSoloLectura]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['es_moroso', 'bloqueado']


class HerramientaViewSet(viewsets.ModelViewSet):
    queryset = Herramienta.objects.all()
    serializer_class = HerramientaSerializer
    permission_classes = [JefeOSoloLectura]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['estado', 'categoria']


class AlquilerViewSet(viewsets.ModelViewSet):
    queryset = Alquiler.objects.all()
    serializer_class = AlquilerSerializer
    permission_classes = [SoloJefeElimina]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['devuelto', 'contratista']


class MantenimientoViewSet(viewsets.ModelViewSet):
    queryset = Mantenimiento.objects.all()
    serializer_class = MantenimientoSerializer
    permission_classes = [JefeOSoloLectura]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['realizado']