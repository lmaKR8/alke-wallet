from pathlib import Path
from django.contrib.messages import constants as messages

# Cargar credenciales de BD desde data/.env.db
def _load_env(path):
    env = {}
    try:
        with open(path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    k, v = line.split('=', 1)
                    env[k.strip()] = v.strip()
    except FileNotFoundError:
        pass
    return env

_DB_ENV = _load_env(Path(__file__).resolve().parent.parent / 'data' / '.env.db')

# ---------------------------------------------------------------------------
# Paths
# --------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent


# ---------------------------------------------------------------------------
# Seguridad — NO usar estos valores en producción
# ---------------------------------------------------------------------------
SECRET_KEY = 'django-insecure-3^li06kk7s)gnhpw2&o^0)*66u4tut-q58o@*#aux+0v-%7xwp'
DEBUG = True
ALLOWED_HOSTS = []


# ---------------------------------------------------------------------------
# Aplicaciones instaladas
# ---------------------------------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Apps del proyecto
    'apps.accounts',
    'apps.wallet',
    'apps.transactions',
    'apps.contacts',
]


# ---------------------------------------------------------------------------
# Middleware — LoginRequiredMiddleware después de AuthenticationMiddleware
# ---------------------------------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'alke_wallet.middleware.LoginRequiredMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'alke_wallet.urls'


# ---------------------------------------------------------------------------
# Templates — directorio centralizado
# ---------------------------------------------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'alke_wallet.wsgi.application'


# ---------------------------------------------------------------------------
# Base de datos (descomentar)
# Desarrollo: SQLite   |   Producción: PostgreSQL
# ---------------------------------------------------------------------------
DATABASES = {
    # Desarrollo SQLite:
    #'default': {
    #    'ENGINE': 'django.db.backends.sqlite3',
    #    'NAME': BASE_DIR / 'db.sqlite3',
    #}

    # Producción PostgreSQL:
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': _DB_ENV.get('DB_NAME', 'alke_wallet'),
        'USER': _DB_ENV.get('DB_USER', 'postgres'),
        'PASSWORD': _DB_ENV.get('DB_PASSWORD', ''),
        'HOST': _DB_ENV.get('DB_HOST', 'localhost'),
        'PORT': _DB_ENV.get('DB_PORT', '5432'),
    }
}


# ---------------------------------------------------------------------------
# Modelo de usuario personalizado
# ---------------------------------------------------------------------------
AUTH_USER_MODEL = 'accounts.User'


# ---------------------------------------------------------------------------
# Validación de contraseñas
# ---------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# ---------------------------------------------------------------------------
# Internacionalización
# ---------------------------------------------------------------------------
LANGUAGE_CODE = 'es-cl'
TIME_ZONE = 'America/Santiago'
USE_I18N = True
USE_TZ = True


# ---------------------------------------------------------------------------
# Archivos estáticos
# ---------------------------------------------------------------------------
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Fixtures
# ---------------------------------------------------------------------------
FIXTURE_DIRS = [BASE_DIR / 'fixtures']


# ---------------------------------------------------------------------------
# Clave primaria por defecto
# ---------------------------------------------------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ---------------------------------------------------------------------------
# Autenticación — redirecciones
# ---------------------------------------------------------------------------
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'login'


# ---------------------------------------------------------------------------
# Mensajes Django → clases CSS Bootstrap
# ---------------------------------------------------------------------------
MESSAGE_TAGS = {
    messages.DEBUG:   'secondary',
    messages.INFO:    'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR:   'danger',
}
