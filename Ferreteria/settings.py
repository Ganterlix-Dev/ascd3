from pathlib import Path
import os
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# Seguridad y debug desde variables de entorno
SECRET_KEY = os.environ.get("SECRET_KEY", "replace-me-locally-only")
DEBUG = True

# Hosts
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "*").split(",")

# Aplicaciones
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "usuarios",
    "ventas",
    "empleado",
    "superadmin",
    "carrito",
    "backups",
    "dbbackup",
    "dbbackup.storage",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # habilitar Whitenoise para archivos estáticos
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "Ferreteria.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "Ferreteria" / "templates",
            BASE_DIR / "usuarios" / "templates",
            BASE_DIR / "ventas" / "templates",
            BASE_DIR / "empleado" / "templates",
            BASE_DIR / "superadmin" / "templates",
            BASE_DIR / "carrito" / "templates",
            BASE_DIR / "backups" / "templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "Ferreteria.wsgi.application"

# Database: usar DATABASE_URL si existe, fallback a configuración local
default_db = {
    "ENGINE": "django.db.backends.postgresql",
    "NAME": "FerreteriaDB",
    "USER": "postgres",
    "PASSWORD": "postgres",
    "HOST": "localhost",
    "PORT": "5432",
}
DATABASES = {"default": dj_database_url.config(default="postgres://postgres:postgres@localhost:5432/FerreteriaDB", conn_max_age=600, ssl_require=False)}
# Si necesitas forzar ssl_require=True en producción, ajusta según Railway.

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

AUTHENTICATION_BACKENDS = ["usuarios.auth_backends.EmailAuthBackend"]
AUTH_USER_MODEL = "usuarios.Personas"

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static and media
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"           # collectstatic escribe aquí en producción
STATICFILES_DIRS = [BASE_DIR / "static"]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"                  # en Railway no es persistente; usar storage externo para uploads

LOGIN_URL = "/Iniciar/"

# Email y dbbackup
EMAIL_BACKEND = os.environ.get("EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend")
DBBACKUP_STORAGE = os.environ.get("DBBACKUP_STORAGE", "django.core.files.storage.FileSystemStorage")
DBBACKUP_STORAGE_OPTIONS = {"location": os.environ.get("DBBACKUP_LOCATION", "/backups/")}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
