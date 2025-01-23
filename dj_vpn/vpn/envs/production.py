from vpn.settings import *

ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=str).split(" ")

SECRET_KEY = config("PROD_SECRET_KEY", cast=str)


INSTALLED_APPS += [
    "corsheaders",
    "storages",
]

MIDDLEWARE.insert(0, "corsheaders.middleware.CorsMiddleware", )
MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware", )

STORAGES = {
    # ...
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3StaticStorage",
    },
}

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "HOST": config("POSTDB_HOST", cast=str),
#         "PASSWORD": config("POSTDB_PASSWORD", cast=str),
#         "PORT": config("POSTDB_PORT", cast=str),
#         "USER": config("POSTDB_USER", cast=str),
#         "NAME": config("POSTDB_NAME", cast=str)
#     }
# }

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": "vpn_postgres",
        "PASSWORD": "vpn.2025",
        "PORT": 5432,
        "USER": "vpn",
        "NAME": "vpndb"
    }
}


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

# django cors header settings
CORS_ALLOW_ALL_ORIGINS = True

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

broker_url = config("BROCKER_URL", cast=str)
result_backend = config("RESULT_BACKEND", cast=str)


