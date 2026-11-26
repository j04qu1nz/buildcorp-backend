from datetime import timedelta

from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.test import APITestCase

from .models import Contratista, Herramienta


class BuildCorpAPITests(APITestCase):
    def setUp(self):
        self.jefe = User.objects.create_superuser('jefe', 'jefe@example.com', 'Clave-Segura-123')
        self.trabajador = User.objects.create_user('obrero', 'obrero@example.com', 'Clave-Segura-123')
        self.contratista = Contratista.objects.create(
            nombre='Juan Pérez', empresa='Constructora Sur', rut='11.111.111-1', telefono='+56912345678')
        self.herramienta = Herramienta.objects.create(codigo='HT-001', nombre='Taladro', categoria='Eléctrica')

    def token(self, usuario, clave='Clave-Segura-123'):
        r = self.client.post('/api/token/', {'username': usuario, 'password': clave}, format='json')
        self.assertEqual(r.status_code, 200)
        return r.data['access']

    def auth(self, usuario):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token(usuario)}')

    def test_sin_token_devuelve_401(self):
        self.assertEqual(self.client.get('/api/herramientas/').status_code, 401)

    def test_health_es_publico(self):
        self.assertEqual(self.client.get('/api/health/').status_code, 200)

    def test_login_incorrecto(self):
        r = self.client.post('/api/token/', {'username': 'jefe', 'password': 'mala'}, format='json')
        self.assertEqual(r.status_code, 401)

    def test_trabajador_puede_leer_pero_no_crear_herramienta(self):
        self.auth('obrero')
        self.assertEqual(self.client.get('/api/herramientas/').status_code, 200)
        r = self.client.post('/api/herramientas/', {'codigo': 'X', 'nombre': 'Y', 'categoria': 'Z'}, format='json')
        self.assertEqual(r.status_code, 403)

    def test_jefe_crud_herramienta(self):
        self.auth('jefe')
        r = self.client.post('/api/herramientas/', {'codigo': 'HT-002', 'nombre': 'Sierra', 'categoria': 'Corte'}, format='json')
        self.assertEqual(r.status_code, 201)
        pk = r.data['id']
        self.assertEqual(self.client.patch(f'/api/herramientas/{pk}/', {'nombre': 'Sierra circular'}, format='json').status_code, 200)
        self.assertEqual(self.client.delete(f'/api/herramientas/{pk}/').status_code, 204)

    def test_validacion_horas_negativas(self):
        self.auth('jefe')
        r = self.client.post('/api/herramientas/', {'codigo': 'HT-003', 'nombre': 'A', 'categoria': 'B',
                                                    'horas_uso_acumuladas': -5}, format='json')
        self.assertEqual(r.status_code, 400)

    def test_alquiler_contratista_bloqueado_da_400(self):
        self.contratista.bloqueado = True
        self.contratista.save()
        self.auth('obrero')
        r = self.client.post('/api/alquileres/', {
            'herramienta': self.herramienta.id, 'contratista': self.contratista.id,
            'fecha_devolucion_estimada': (timezone.now() + timedelta(days=2)).isoformat(),
            'firma_digital': 'Firmado'}, format='json')
        self.assertEqual(r.status_code, 400)

    def test_alquiler_ok_y_solo_jefe_elimina(self):
        self.auth('obrero')
        r = self.client.post('/api/alquileres/', {
            'herramienta': self.herramienta.id, 'contratista': self.contratista.id,
            'fecha_devolucion_estimada': (timezone.now() + timedelta(days=2)).isoformat(),
            'firma_digital': 'Firmado'}, format='json')
        self.assertEqual(r.status_code, 201)
        pk = r.data['id']
        self.assertEqual(self.client.delete(f'/api/alquileres/{pk}/').status_code, 403)
        self.auth('jefe')
        self.assertEqual(self.client.delete(f'/api/alquileres/{pk}/').status_code, 204)