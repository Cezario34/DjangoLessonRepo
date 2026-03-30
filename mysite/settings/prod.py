from .base import *

DEBUG = False

ADMINS = [
    ('Cezario', 'coltey9@gmail.com'),
]

ALLOWED_HOSTS = ['ladaorfeeva.ru', 'www.ladaorfeeva.ru']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Security
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True