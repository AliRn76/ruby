"""
Django settings for ruby project.
Author Ali RajabNezhad 17 May 2022
"""
import redis
from pathlib import Path
from datetime import timedelta
from dotenv import dotenv_values

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

config = dotenv_values(BASE_DIR / '.secret_keys')

SECRET_KEY = config['SECRET_KEY']
    
MYSQL_DB = config['MYSQL_DB']
MYSQL_USER = config['MYSQL_USER']
MYSQL_PASS = config['MYSQL_PASS']
MYSQL_HOST = config['MYSQL_HOST']
MYSQL_PORT = config['MYSQL_PORT']

REDIS_HOST = config['REDIS_HOST']
REDIS_PORT = config['REDIS_PORT']

OTP_EXP_SECOND = int(config['OTP_EXP_SECOND'])

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'user',
    'pv',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'configs.urls'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'user.authentication.JWTAuthentication',
    ],
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    # TODO: Set Custom Throttling For Get And Post
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '20/min',
        'user': '60/min'
    },
}

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

WSGI_APPLICATION = 'configs.wsgi.application'
ASGI_APPLICATION = 'websocket.routings.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [(REDIS_HOST, REDIS_PORT)],
            'channel_capacity': {
                'http.request': 1000,
                'websocket.send*': 1000
            },
            'capacity': 1000
        },
    },
}


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': MYSQL_DB,
#         'USER': MYSQL_USER,
#         'HOST': MYSQL_HOST,
#         'PORT': MYSQL_PORT,
#         'PASSWORD': MYSQL_PASS,
#         'TEST': {
#             'CHARSET': 'utf8',
#             'COLLATION': 'utf8_general_ci',
#         },
#     },
# }

REDIS_CONNECTION_POOL = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=0)
REDIS: redis.Redis = redis.Redis(connection_pool=REDIS_CONNECTION_POOL)

REDIS_ONLINE_USERS_CONNECTION_POOL = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=1)
REDIS_ONLINE_USERS: redis.Redis = redis.Redis(connection_pool=REDIS_ONLINE_USERS_CONNECTION_POOL)

REDIS_UNREAD_MESSAGES_CONNECTION_POOL = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=2)
REDIS_UNREAD_MESSAGES: redis.Redis = redis.Redis(connection_pool=REDIS_UNREAD_MESSAGES_CONNECTION_POOL)

PV_EXP_TIME = timedelta(days=2).total_seconds()
GROUP_EXP_TIME = timedelta(days=7).total_seconds()

OTP_LEN = 4

AUTH_USER_MODEL = 'user.User'


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_TZ = True

APPEND_SLASH = False

STATIC_ROOT = BASE_DIR / 'static'
STATIC_URL = 'static/'

MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = 'media/'
