"""
Django settings for ams project.

Generated by 'django-admin startproject' using Django 4.2.16.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent
from decouple import config

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-491rni3mumgwh#k2_-&0w+t^_^_@hu4f(^$d1i$tubsuv9!0x1'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "ams.apps.custom_auth",
    "ams.apps.core_ams",
    'rest_framework',
    "drf_yasg",
    'rest_framework.authtoken',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'ams.apps.custom_auth.authsetup.MiddlewarePrintRequest'
    "ams.middleware.RequestResponseLoggingMiddleware"
]

ROOT_URLCONF = 'ams.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ams.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# This is to connect locally added pg admin with this django app
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',  # Correct backend for PostgreSQL
#         'NAME': 'ams', # database name
#         'USER': 'mac',  # Make sure this matches the PostgreSQL username
#         'PASSWORD': 'Password1',  # Make sure this matches the PostgreSQL password
#         'HOST': '127.0.0.1',  # localhost
#         'PORT': '5432',  # default PostgreSQL port
#     }
# }

# HOST = config('HOST', default='', cast=str)
# if HOST == "test":
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }
# elif HOST == "development":
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.postgresql_psycopg2',  # Correct backend for PostgreSQL
#             'NAME': config('POSTGRES_DB', default='', cast=str), # Database name (must match POSTGRES_DB in docker-compose)
#             'USER': config('POSTGRES_USER', default='', cast=str), # Database user (must match POSTGRES_USER in docker-compose)
#             'PASSWORD': config('POSTGRES_PASSWORD', default='', cast=str), # Database password (must match POSTGRES_PASSWORD in docker-compose)
#             'HOST': 'db',  # The name of the database service in docker-compose
#             'PORT': '5432',  # Default PostgreSQL port
#         }
#     }
# else :
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.postgresql_psycopg2',  # Correct backend for PostgreSQL
#             'NAME': config('POSTGRES_DB', default='', cast=str), # Database name (must match POSTGRES_DB in docker-compose)
#             'USER': config('POSTGRES_USER', default='', cast=str), # Database user (must match POSTGRES_USER in docker-compose)
#             'PASSWORD': config('POSTGRES_PASSWORD', default='', cast=str), # Database password (must match POSTGRES_PASSWORD in docker-compose)
#             'HOST': 'db',  # The name of the database service in docker-compose
#             'PORT': '5432',  # Default PostgreSQL port
#         }
#     }

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',  # Correct backend for PostgreSQL
#         'NAME': "postgres",  # Database name (must match POSTGRES_DB in docker-compose)
#         'USER': "postgres",# Database user (must match POSTGRES_USER in docker-compose)
#         'PASSWORD': "root",# Database password (must match POSTGRES_PASSWORD in docker-compose)
#         'HOST': 'db',  # The name of the database service in docker-compose
#         'PORT': '5432',  # Default PostgreSQL port
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',  # Correct backend for PostgreSQL
        'NAME': "postgres",  # Database name (must match POSTGRES_DB in StatefulSet)
        'USER': "postgres",  # Database user (must match POSTGRES_USER in StatefulSet)
        'PASSWORD': "root",  # Database password (change this to securely fetch from Kubernetes secrets)
        'HOST': 'postgres',  # The name of the PostgreSQL service in Kubernetes
        'PORT': '5432',  # Default PostgreSQL port
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'custom_auth.Users'
AUTHENTICATION_BACKENDS = ["ams.apps.custom_auth.authsetup.UserAuthentication"]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
}

CSRF_TRUSTED_ORIGINS = [
    'https://a133-2401-4900-8fc8-e860-1c3e-f6fc-e8ad-bbaa.ngrok-free.app',
]

SWAGGER_SETTINGS = {
    'SHOW_REQUEST_HEADERS': True,
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    },
    'USE_SESSION_AUTH': False,
    'JSON_EDITOR': True,
    'SUPPORTED_SUBMIT_METHODS': [
        'get',
        'post',
        'put',
        'delete',
        'patch'
    ],
}

# CACHES = {
#     'default': {
#         'BACKEND': 'django_redis.cache.RedisCache',
#         'LOCATION': 'redis://127.0.0.1:6379/1',  # Redis instance running on localhost, DB 1
#         'OPTIONS': {
#             'CLIENT_CLASS': 'django_redis.client.DefaultClient',
#         }
#     }
# }


# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'file': {
#             'level': 'DEBUG',
#             'class': 'logging.FileHandler',
#             'filename': 'django_requests.log',
#         },
#         'console': {
#             'level': 'DEBUG',
#             'class': 'logging.StreamHandler',
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['file', 'console'],
#             'level': 'DEBUG',
#             'propagate': True,
#         },
#     },
# }


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        # Console handler for real-time logging (e.g., useful in development or when using a process manager like Gunicorn)
        'console': {
            'level': 'WARNING',  # Only log warnings and errors to the console in production
            'class': 'logging.StreamHandler',
        },
        # File handler for general logs, with rotation to prevent file overflow
        'file': {
            'level': 'INFO',  # Log INFO level and higher to files (errors, important events)
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'django_requests.log',  # Log file for requests
            'maxBytes': 1024 * 1024 * 10,  # Maximum size of log file (10 MB in this example)
            'backupCount': 5,  # Keep 5 old log files (older logs will be archived)
        },
        # Error log file handler (separate from general logs)
        'error_file': {
            'level': 'ERROR',  # Only log errors to this file
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'django_error.log',
            'maxBytes': 1024 * 1024 * 10,  # 10 MB size limit
            'backupCount': 5,  # Keep 5 old error logs
        },
        # Optional: Error logging to external services like Sentry
        # 'sentry': {
        #     'level': 'ERROR',  # Log only errors to external logging service
        #     'class': 'raven.handlers.logging.SentryHandler',
        #     'dsn': 'your_sentry_dsn_here',
        # },
    },
    'loggers': {
        # General logger for Django-related logs
        'django': {
            'handlers': ['console', 'file', 'error_file'],  # Log to console, files, and error log
            'level': 'INFO',  # Log INFO level and higher (errors, warnings, info)
            'propagate': True,  # Allow logs to propagate to parent loggers
        },
        # Loggers for specific applications can be added here if needed
        # Example:
        # 'django.db.backends': {
        #     'handlers': ['file'],
        #     'level': 'ERROR',
        #     'propagate': False,
        # },
    },
}


# LOGGING = {
#
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'console': {
#             'level': 'INFO',  # Log level for console (stdout)
#             'class': 'logging.StreamHandler',
#             'stream': 'ext://sys.stdout',  # Send logs to stdout
#         },
#         'file': {
#             'level': 'INFO',
#             'class': 'logging.handlers.RotatingFileHandler',
#             'filename': '/var/log/django/django_requests.log',  # Log files inside container
#             'maxBytes': 1024 * 1024 * 10,  # 10 MB file size limit
#             'backupCount': 5,  # Keep up to 5 backup files
#         },
#
#         'error_file': {
#             'level': 'ERROR',  # Log level for errors
#             'class': 'logging.handlers.RotatingFileHandler',
#             'filename': '/var/log/django/django_error.log',  # Log errors inside container
#             'maxBytes': 1024 * 1024 * 10,  # 10 MB file size limit
#             'backupCount': 5,  # Keep up to 5 backup error files
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['console', 'file', 'error_file'],  # Output to console, file, and error file
#             'level': 'INFO',  # Log level (INFO, ERROR, etc.)
#             'propagate': True,
#         },
#     },
# }

# DEBUG, INFO, WARNING, ERROR, CRITICAL

