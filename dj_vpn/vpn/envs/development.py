from dj_vpn.vpn.settings import *

SECRET_KEY = config("DEV_SECRET_KEY", cast=str)

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
    },
    "second_db": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("PUB_POSTDB_NAME", cast=str),
        "USER": config("PUB_POSTDB_USER", cast=str),
        "PASSWORD": config("PUB_POSTDB_PASSWORD", cast=str),
        "HOST": config("PUB_POSTDB_HOST", cast=str),
        "PORT": config("PUB_POSTDB_PORT", cast=str),
    }
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

CACHES["default"]["LOCATION"] = "redis://localhost:6379/2"

broker_url = "redis://localhost:6379/0"
result_backend = "redis://localhost:6379/1"

# with logging django
log_dir = os.path.join(BASE_DIR / "general_log_django", datetime.now().strftime("%Y-%m-%d"))
os.makedirs(log_dir, exist_ok=True)
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "color": {
            "()": "colorlog.ColoredFormatter",
            "format": "%(log_color)s%(levelname)s %(reset)s%(asctime)s %(module)s %(process)d %(thread)d %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "filters": {
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "color",
            "filters": ["require_debug_true"],
        },
        "info_file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "formatter": "color",
            "filename": os.path.join(BASE_DIR / log_dir / "info_file.log")
        },
        "error_file": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "formatter": "color",
            "filename": os.path.join(BASE_DIR / log_dir / "error_file.log")
        },
        "warning_file": {
            "level": "WARN",
            "class": "logging.FileHandler",
            "formatter": "color",
            "filename": os.path.join(BASE_DIR / log_dir / "warning_file.log")
        },
        "critical_file": {
            "level": "CRITICAL",
            "class": "logging.FileHandler",
            "formatter": "color",
            "filename": os.path.join(BASE_DIR / log_dir / "critical_file.log")
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console", "info_file", "warning_file", "critical_file", "error_file"],
            "propagate": True,
        }
    }
}