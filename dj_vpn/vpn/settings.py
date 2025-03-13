import os
from datetime import timedelta
from pathlib import Path

from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", default=False, cast=bool)

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "import_export",
    "django_celery_beat",
    "django_celery_results",
    "axes",
    "drf_spectacular",
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    # "guardian",

    "dj_vpn.accounts.apps.AccountsConfig",
    "dj_vpn.configs.apps.ConfigsConfig",
    "dj_vpn.cores.apps.CoresConfig",
    "dj_vpn.main_settings.apps.MainSettingsConfig"
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # "accounts.middleware.LogMiddleware"
    "axes.middleware.AxesMiddleware",
    "dj_vpn.vpn.utils.middleware.CheckDeviceBlockMiddleware",
    # "dj_cpn.vpn.utils.middleware.CheckLoginMiddleware"

]

ROOT_URLCONF = "dj_vpn.vpn.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "dj_vpn.vpn.wsgi.application"

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Tehran"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/
STATIC_URL = "static/static/"
STATIC_ROOT = os.path.join(BASE_DIR / "staticfiles")
MEDIA_URL = "static/media/"
MEDIA_ROOT = os.path.join(BASE_DIR / "media")
# STATICFILES_DIRS = [
#     BASE_DIR / "static"
# ]

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "accounts.User"

# JET_PROJECT = 'vpn_4'
# JET_TOKEN = config("JET_TOKEN")

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",

}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=365),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=30),
    "AUTH_HEADER_TYPES": ("Bearer",),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True
}

SPECTACULAR_SETTINGS = {
    "TITLE": "vpn project",
    "DESCRIPTION": "vpn project",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}


AXES_FAILURE_LIMIT = 10
AXES_LOCK_OUT_FAILURE = True
AXES_LOCKOUT_TIME = timedelta(hours=1)
AXES_COOLOFF_TIME = timedelta(minutes=10)
AXES_CACHE = "default"
# AXES_LOCKOUT_CALLABLE = 'api.v1.accounts.views.show_block'
AXES_LOCKOUT_TEMPLATE = None

CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"

DJANGO_CELERY_RESULTS_TASK_ID_MAX_LENGTH = 191

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesStandaloneBackend',
    'django.contrib.auth.backends.ModelBackend',
    # 'guardian.backends.ObjectPermissionBackend',
]
