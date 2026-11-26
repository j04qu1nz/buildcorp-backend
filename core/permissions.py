from rest_framework.permissions import SAFE_METHODS, BasePermission


class JefeOSoloLectura(BasePermission):
    """Usuarios autenticados pueden consultar; solo el Jefe (superusuario) puede crear, editar o eliminar."""

    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_superuser


class SoloJefeElimina(BasePermission):
    """Usuarios autenticados pueden consultar, crear y editar; solo el Jefe puede eliminar."""

    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        if request.method == 'DELETE':
            return request.user.is_superuser
        return True