import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

sys.path.insert(0, BASE_DIR.as_posix())

SECRET_KEY = 'secret'  # noqa: S105
DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    "test_api",
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "rest_framework",
]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
]

ROOT_URLCONF = 'core.urls'

DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}}

REST_FRAMEWORK = {
    "EXCEPTION_HANDLER": "verbose_http_exceptions.ext.django.exception_handler",
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.BasicAuthentication",
    ],
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
