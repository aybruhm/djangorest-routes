from djangorest_routes.config.base import *


DEBUG = env("DEBUG")


# HASH_FIELD_SALT WARNING: keep the salt key used in production secret!
HASH_FIELD_SALT = "k^8p7869&jh9w7jhtnjun!di55o$rg0*g%mdi(_-3xue#)e=(!"


ALLOWED_HOSTS += ["127.0.0.1", "localhost"]


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Application Definition

INSTALLED_APPS += []

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATIC_URL = "/static/"


# Email Configuration

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
DEFAULT_FROM_EMAIL = "djangorest-auth@digitalstade.com"
