from djangorest_routes.config.base import *


DEBUG = env("DEBUG")

ALLOWED_HOSTS += ["djangorest_auth.digitalstade.com", "djangorest_auth.herokuapp.com"]


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    "default": dj_database_url.parse(env("DATABASE_URL")),
}

# Application Definition

INSTALLED_APPS += []

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_ROOT = "staticfiles"
STATIC_URL = "/static/"


# EMAIL CONFIGURATION
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"

EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_PORT = env("EMAIL_PORT")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")

EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


# HTTPS SETTINGS
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 99999990
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
