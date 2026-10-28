from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views import ContratistaViewSet, HerramientaViewSet, AlquilerViewSet, MantenimientoViewSet

# Importaciones para drf-spectacular
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

router = DefaultRouter()
router.register(r'contratistas', ContratistaViewSet)
router.register(r'herramientas', HerramientaViewSet)
router.register(r'alquileres', AlquilerViewSet)
router.register(r'mantenimientos', MantenimientoViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    
    # Rutas de la documentación con drf-spectacular
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]