"""
Django settings for APSocial project.

Generated by 'django-admin startproject' using Django 5.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import os
from datetime import timedelta
from pathlib import Path
import logging
import django
from django.utils.encoding import smart_str
from django.utils.translation import gettext
from django.template.context_processors import media

django.utils.encoding.smart_text = smart_str
django.utils.translation.ugettext = gettext

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-ccd6214@*gar_$sl%evmta@1&e+o33(og$h-2d=&3oe9y0#@y+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'apricop05@gmail.com'
EMAIL_HOST_PASSWORD = 'rvmj caxr awzu iyui'

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    "daphne",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_filters',
    'channels',
    'users',
    'chat',
]

ASGI_APPLICATION = "APSocial.asgi.application"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
CORS_ORIGIN_ALLOW_ALL = True
ROOT_URLCONF = "APSocial.urls"

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

WSGI_APPLICATION = 'APSocial.wsgi.application'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'channels': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}

AUTH_USER_MODEL = 'users.Users'

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DATETIME_FORMAT': "%d/%m/%Y %H:%M:%S",
    'DATE_FORMAT': "%d/%m/%Y"
}

JWT_AUTH = {
    "JWT_ENCODE_HANDLER": "rest_framework_jwt.utils.jwt_encode_handler",
    "JWT_DECODE_HANDLER": "rest_framework_jwt.utils.jwt_decode_handler",
    "JWT_PAYLOAD_HANDLER": "rest_framework_jwt.utils.jwt_payload_handler",
    "JWT_PAYLOAD_GET_USER_ID_HANDLER": "rest_framework_jwt.utils.jwt_get_user_id_from_payload_handler",  # noqa
    "JWT_RESPONSE_PAYLOAD_HANDLER": "rest_framework_jwt.utils.jwt_response_payload_handler",  # noqa
    "JWT_SECRET_KEY": SECRET_KEY,
    "JWT_GET_USER_SECRET_KEY": None,
    "JWT_PUBLIC_KEY": None,
    "JWT_PRIVATE_KEY": None,
    "JWT_ALGORITHM": "HS256",
    "JWT_VERIFY": True,
    "JWT_VERIFY_EXPIRATION": True,
    "JWT_LEEWAY": 0,
    "JWT_EXPIRATION_DELTA": timedelta(days=30),
    "JWT_AUDIENCE": None,
    "JWT_ISSUER": None,
    "JWT_ALLOW_REFRESH": True,
    "JWT_REFRESH_EXPIRATION_DELTA": timedelta(days=30),
    "JWT_AUTH_HEADER_PREFIX": "Bearer",
    "JWT_AUTH_COOKIE": None,
}

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True
CORS_ALLOW_ALL_ORIGINS = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
