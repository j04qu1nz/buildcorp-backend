from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path
from drf_spectacular.utils import extend_schema
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from core.views import AlquilerViewSet, ContratistaViewSet, HerramientaViewSet, MantenimientoViewSet

router = DefaultRouter()
router.register(r'contratistas', ContratistaViewSet)
router.register(r'herramientas', HerramientaViewSet)
router.register(r'alquileres', AlquilerViewSet)
router.register(r'mantenimientos', MantenimientoViewSet)


@extend_schema(exclude=True)
@api_view(['GET'])
@permission_classes([AllowAny])
def health(request):
    """Endpoint público y liviano: sirve para probar API Gateway y su rate limit."""
    return JsonResponse({'status': 'ok'})


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/health/', health, name='health'),

    # Autenticación JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Documentación con drf-spectacular
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]