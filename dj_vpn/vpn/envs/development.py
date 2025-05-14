from dj_vpn.vpn.settings import *

SECRET_KEY = config("DEV_SECRET_KEY", cast=str)

ALLOWED_HOSTS = []

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": "localhost",
        "PASSWORD": "postgres",
        "PORT": "5433",
        "USER": "postgres",
        "NAME": "vpndb"
    },
    # "second_db": {
    #     "ENGINE": "django.db.backends.postgresql",
    #     "NAME": config("PUB_POSTDB_NAME", cast=str),
    #     "USER": config("PUB_POSTDB_USER", cast=str),
    #     "PASSWORD": config("PUB_POSTDB_PASSWORD", cast=str),
    #     "HOST": config("PUB_POSTDB_HOST", cast=str),
    #     "PORT": config("PUB_POSTDB_PORT", cast=str),
    # }
}

# JET_TOKEN = config("JET_TOKEN", cast=str)

INSTALLED_APPS += [
    "debug_toolbar",
    "django_extensions",
]

MIDDLEWARE += [
    #     debug toolbar middlewere
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

# The Debug Toolbar is shown only if your IP address is listed in Django’s INTERNAL_IPS setting.
INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]

SIMPLE_JWT["SIGNING_KEY"] = SECRET_KEY

CACHES["default"]["LOCATION"] = "redis://localhost:6380/2"

CELERY_BROKER_URL = "redis://localhost:6380/0"
CELERY_RESULT_BACKEND = "redis://localhost:6380/0"

