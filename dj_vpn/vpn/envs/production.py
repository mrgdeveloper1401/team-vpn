from dj_vpn.vpn.settings import *

ALLOWED_HOSTS = config("VPS_ALLOWD_HOSTS", cast=str).split(" ")


SECRET_KEY = config("PROD_SECRET_KEY", cast=str)

INSTALLED_APPS += [
    "corsheaders",
    "storages",
]

MIDDLEWARE.insert(0, "corsheaders.middleware.CorsMiddleware", )
# MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware", )

STORAGES = {
    "staticfiles": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    }
}

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": config("VPS_POSTDB_HOST", cast=str),
        "PASSWORD": config("VPS_POSTDB_PASSWORD", cast=str),
        "PORT": config("VPS_POSTDB_PORT", cast=str),
        "USER": config("VPS_POSTDB_USER", cast=str),
        "NAME": config("VPS_POSTDB_NAME", cast=str)
    }
}

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "HOST": config("DOCKER_POSTGRES_HOST", cast=str),
#         "PASSWORD": config("DOCKER_POSTGRES_PASSWORD", cast=str),
#         "PORT": 5432,
#         "USER": config("DOCKER_POSTGRES_USER", cast=str),
#         "NAME": config("DOCKER_POSTGRES_DB", cast=str),
#     }
# }


# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "HOST": config("PUB_POSTDB_HOST", cast=str),
#         "PASSWORD": config("PUB_POSTDB_PASSWORD", cast=str),
#         "PORT": config("PUB_POSTDB_PORT", cast=str),
#         "USER": config("PUB_POSTDB_USER", cast=str),
#         "NAME": config("PUB_POSTDB_NAME", cast=str)
#     }
# }

# when test production model we can use these databases
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": "postgres",
#         "USER": "postgres",
#         "PASSWORD": "postgres",
#         "HOST": "localhost",
#         "PORT": "5433",
#     }
# }

# django cors header settings
# CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOWED_ORIGINS = [
    "https://194.156.103.14"
]

# ssl config
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = "SAMEORIGIN"
SECURE_REFERRER_POLICY = "strict-origin"
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# aws config
# AWS_ACCESS_KEY_ID = config("ARVAN_ACCESS_KEY", cast=str)
# AWS_SECRET_ACCESS_KEY = config("ARVAN_SECRET_KET", cast=str)
# AWS_STORAGE_BUCKET_NAME = config("ARVAN_STORAGE_BUCKET_NAME", cast=str)
# AWS_S3_FILE_OVERWRITE = False
# AWS_SERVICE_NAME = 's3'
# AWS_S3_REGION_NAME = 'us-east-1'
# AWS_S3_ENDPOINT_URL = config("AWS_S3_DOMAIN", cast=str)

SIMPLE_JWT["SIGNING_KEY"] = SECRET_KEY

broker_url = config("VPS_BROCKER_URL", cast=str)
result_backend = config("VPS_RESULT_BACKEND", cast=str)
