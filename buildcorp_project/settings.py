"""
Django settings for buildcorp_project project.

Todas las credenciales y valores sensibles se leen desde variables de
entorno (ver .env.example). No se guarda ningún secreto en el repositorio.
"""

import os
from datetime import timedelta
from pathlib import Path

from django.core.management.utils import get_random_secret_key

BASE_DIR = Path(__file__).resolve().parent.parent


def env_bool(nombre, por_defecto=False):
    return os.environ.get(nombre, str(por_defecto)).strip().lower() in ('1', 'true', 'yes', 'si')


# --- Seguridad básica -------------------------------------------------------
DEBUG = env_bool('DJANGO_DEBUG', False)

# En producción DJANGO_SECRET_KEY es obligatoria. Solo en DEBUG se genera una
# clave aleatoria temporal (no queda ningún secreto escrito en el código).
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
if not SECRET_KEY:
    if DEBUG:
        SECRET_KEY = get_random_secret_key()
    else:
        raise RuntimeError('Falta la variable de entorno DJANGO_SECRET_KEY')

ALLOWED_HOSTS = [h.strip() for h in os.environ.get('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',') if h.strip()]

# Activar solo cuando el sitio se sirva por HTTPS (cookies solo por canal seguro)
USE_HTTPS = env_bool('DJANGO_USE_HTTPS', False)
SESSION_COOKIE_SECURE = USE_HTTPS
CSRF_COOKIE_SECURE = USE_HTTPS
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'


# --- Aplicaciones -----------------------------------------------------------
INSTALLED_APPS = [
    'jazzmin',  # debe ir antes de django.contrib.admin
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'rest_framework_simplejwt',
    'django_filters',
    'drf_spectacular',
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'buildcorp_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'buildcorp_project.wsgi.application'


# --- Base de datos ----------------------------------------------------------
# Si DB_HOST está definida se usa PostgreSQL (RDS); si no, SQLite para desarrollo local.
if os.environ.get('DB_HOST'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('DB_NAME', 'buildcorp_db'),
            'USER': os.environ['DB_USER'],
            'PASSWORD': os.environ['DB_PASSWORD'],
            'HOST': os.environ['DB_HOST'],
            'PORT': os.environ.get('DB_PORT', '5432'),
            # TLS hacia RDS (evidencia de protección del tráfico)
            'OPTIONS': {'sslmode': os.environ.get('DB_SSLMODE', 'require')},
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# --- Validación de contraseñas ----------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# --- Internacionalización ---------------------------------------------------
LANGUAGE_CODE = 'es-cl'
TIME_ZONE = 'America/Santiago'
USE_I18N = True
USE_TZ = True


# --- Archivos estáticos -----------------------------------------------------
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# --- CORS (frontend en otra EC2) --------------------------------------------
# Ejemplo: CORS_ALLOWED_ORIGINS=http://IP_FRONTEND,http://localhost:5173
CORS_ALLOWED_ORIGINS = [o.strip() for o in os.environ.get('CORS_ALLOWED_ORIGINS', '').split(',') if o.strip()]


# --- Django REST Framework + JWT --------------------------------------------
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    # Por defecto todo endpoint exige un JWT válido
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'AUTH_HEADER_TYPES': ('Bearer',),
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'BuildCorp API',
    'DESCRIPTION': 'Documentación oficial de la API de Control y Alquiler de Herramientas BuildCorp',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}


# --- Jazzmin (admin) --------------------------------------------------------
JAZZMIN_SETTINGS = {
    "site_title": "BuildCorp Admin",
    "site_header": "BuildCorp",
    "site_brand": "BuildCorp Control",
    "welcome_sign": "Bienvenido al Sistema de Gestión BuildCorp",
    "copyright": "BuildCorp Ltda.",
    "icons": {
        "auth.user": "fas fa-user-shield",
        "auth.Group": "fas fa-users",
        "core.contratista": "fas fa-hard-hat",
        "core.herramienta": "fas fa-tools",
        "core.alquiler": "fas fa-file-contract",
        "core.mantenimiento": "fas fa-wrench",
    },
    "show_sidebar": True,
    "navigation_expanded": True,
    "custom_css": None,
    "custom_js": None,
}

JAZZMIN_UI_TWEAKS = {
    "theme": "slate",
    "dark_mode_theme": "slate",
}