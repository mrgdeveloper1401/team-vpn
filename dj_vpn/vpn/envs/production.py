from dj_vpn.vpn.settings import *

# use in vps
ALLOWED_HOSTS = ''.join(config("VPS_ALLOWED_HOSTS", cast=list)).split(",")

# for test use
# ALLOWED_HOSTS = ["*"]

SECRET_KEY = config("PROD_SECRET_KEY", cast=str)

INSTALLED_APPS += [
    "corsheaders",
    "storages",
]

MIDDLEWARE.insert(0, "corsheaders.middleware.CorsMiddleware",)
MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")

STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    }
}

# use docker in vps
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": config("VPS_POSTDB_HOST", cast=str),
        "PASSWORD": config("VPS_POSTDB_PASSWORD", cast=str),
        "PORT": config("VPS_POSTDB_PORT", cast=str),
        "USER": config("VPS_POSTDB_USER", cast=str),
        "NAME": config("VPS_POSTDB_NAME", cast=str)
    },
    "OPTIONS": {
        "pool": {
            "min_size": 1,
            "max_size": 2,
            "timeout": 10
        }
    }
}

# use docker in my local system
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

# use port public in vps
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "HOST": config("PUB_KUBAR_POSTDB_HOST", cast=str),
#         "PASSWORD": config("PUB_KUBAR_POSTDB_PASSWORD", cast=str),
#         "PORT": config("PUB_KUBAR_POSTDB_PORT", cast=str),
#         "USER": config("PUB_KUBAR_POSTDB_USER", cast=str),
#         "NAME": config("PUB_KUBAR_POSTDB_NAME", cast=str)
#     }
# }

# use in the system, database postgresql
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
# if we can test and develop api this button we can set
# CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOWED_ORIGINS = "".join(config("PROD_CORS_ORIGIN", cast=list)).split(",")

# secure header config
SESSION_COOKIE_SECURE = True # send cookie only https
CSRF_COOKIE_SECURE = True # send csrf cookie only https
SECURE_SSL_REDIRECT = True # redirect http into https
SECURE_HSTS_SECONDS = 31536000 # time active http strict transport security
SECURE_HSTS_PRELOAD = True # preload hsts, use browser before preload view site use https
SECURE_HSTS_INCLUDE_SUBDOMAINS = True # use hsts for all subdomain
SECURE_CONTENT_TYPE_NOSNIFF = True # prevent sniffing mime
SECURE_BROWSER_XSS_FILTER = True # active filter xss
X_FRAME_OPTIONS = "SAMEORIGIN" # prevent show iframe tags, prevent attack clickjacking
SECURE_REFERRER_POLICY = "strict-origin" # what send information in header
USE_X_FORWARDED_HOST = True # suitable proxy pass
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https") # secure connection django in proxy pass

# aws config
# AWS_ACCESS_KEY_ID = config("ARVAN_ACCESS_KEY", cast=str)
# AWS_SECRET_ACCESS_KEY = config("ARVAN_SECRET_KET", cast=str)
# AWS_STORAGE_BUCKET_NAME = config("ARVAN_STORAGE_BUCKET_NAME", cast=str)
# AWS_S3_FILE_OVERWRITE = False
# AWS_SERVICE_NAME = 's3'
# AWS_S3_REGION_NAME = 'us-east-1'
# AWS_S3_ENDPOINT_URL = config("AWS_S3_DOMAIN", cast=str)

SIMPLE_JWT["SIGNING_KEY"] = SECRET_KEY
SIMPLE_JWT["ALGORITHM"] = config("VPS_JWT_ALGORITHM", cast=str, default="HS256")
# inactive previous refresh token
SIMPLE_JWT['ROTATE_REFRESH_TOKENS'] = config("ROTATE_REFRESH_TOKENS", cast=bool, default=True)
# active black list token, possible disable token before expired
SIMPLE_JWT['BLACKLIST_AFTER_ROTATION'] = config("BLACKLIST_AFTER_ROTATION", cast=bool, default=True)
SIMPLE_JWT['AUTH_HEADER_TYPES'] = tuple(''.join(config("AUTH_HEADER_TYPES", cast=tuple, default=("Bearer",))).split(","))
SIMPLE_JWT['AUTH_HEADER_NAME'] = config("AUTH_HEADER_NAME", cast=str, default="HTTP_AUTHORIZATION")
SIMPLE_JWT['AUDIENCE'] = config("AUTH_AUDIENCE", cast=str, default="") # this url can use token
SIMPLE_JWT["ISSUER"] = config("AUTH_ISSUER", cast=str, default="") # prevent use fake token, helpful identify microservice
SIMPLE_JWT["LEEWAY"] = config("LEEWAY", cast=int, default=0) # Taking advantage of the time difference

CELERY_BROKER_URL = config("CELERY_BROKER_URL", cast=str)
CELERY_RESULT_BACKEND = config("CELERY_RESULT_BACKEND", cast=str)

CACHES["default"]["LOCATION"] = "redis://vpn_redis:6379/2"
