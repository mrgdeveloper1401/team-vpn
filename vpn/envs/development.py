from vpn.settings import *


SECRET_KEY = config('DEV_SECRET_KEY', cast=str)


ALLOWED_HOSTS = []


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": "localhost",
        "PASSWORD": "postgres",
        "PORT": "5432",
        "USER": "postgres",
        "NAME": "vpndb"
    }
}

# JET_TOKEN = config("JET_TOKEN", cast=str)

INSTALLED_APPS += [
    "debug_toolbar",
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
