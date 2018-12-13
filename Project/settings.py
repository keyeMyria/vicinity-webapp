
import os
import time
import configparser
from celery.schedules import crontab

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR_SETTING = BASE_DIR + '/Project/setting_ini/setting.ini'

config = configparser.ConfigParser()

config.read(BASE_DIR_SETTING)

DATABASE_NAME = config.get('database', 'DATABASE_NAME')
DATABASE_USER = config.get('database', 'DATABASE_USER')
DATABASE_PASSWORD = config.get('database', 'DATABASE_PASSWORD')
DATABASE_HOST = config.get('database', 'DATABASE_HOST')
DATABASE_PORT = config.get('database', 'DATABASE_PORT')
PROJECT_NAME = config.get('project', 'PROJECT_NAME')
PROJECT_ICON = config.get('project', 'PROJECT_ICON')
GOOGLE_API_KEY = config.get('api', 'GOOGLE_API_KEY')
GOOGLE_API_KEY_FRONT = config.get('api', 'GOOGLE_API_KEY_FRONT')
EMAIL_SERVER_HOST = config.get('email', 'EMAIL_HOST')
EMAIL_USER = config.get('email', 'EMAIL_HOST_USER')
EMAIL_PASSWORD = config.get('email', 'EMAIL_HOST_PASSWORD')

SECRET_KEY = 'id(hu83#rztzvol744vwzu_8)_^xan#i7^f)kg7wrj62-m(pkc'


WEBAPP_NOCACHE_TOKEN = "?" + str(int(time.time()))

DEBUG_DATA = config.get('project', 'DEBUG')

if DEBUG_DATA:
    DEBUG = DEBUG_DATA
else:
    DEBUG = False

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social_django',
    'backend',
    'frontend',
    'accounts',

    'ckeditor',
    'ckeditor_uploader',

    'core',
    'spaceadmin',
    'contact',
    'about',
    'managerooms',
    
    'import_export',    
    'channels',
    'django.contrib.sites',
    'django.contrib.sitemaps',
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

ROOT_URLCONF = 'Project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'backend.context_processor.base',
                   'social_django.context_processors.backends',
                   'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'Project.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': DATABASE_NAME,
        'USER': DATABASE_USER,
        'PASSWORD': DATABASE_PASSWORD,
        'HOST': DATABASE_HOST,
        'PORT': DATABASE_PORT,
        'OPTIONS': {
            'init_command': 'SET foreign_key_checks = 0;',
        },
    }
}

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

IMPORT_EXPORT_USE_TRANSACTIONS = True

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

STATIC_URL = '/static/'

if not DEBUG:
    STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static", "admin"),
    )

    STATIC_ROOT = os.path.join(BASE_DIR, 'static')
else:
     
    STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static", "admin"),
    os.path.join(BASE_DIR, 'static'),
    )

SITE_ID = 1


CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_CONFIGS = {
    'default': {
        'width': 850,
        'height': 350,
        'filebrowserWindowWidth': 975,
        'filebrowserWindowHeight': 550,
    },
    'small': {
        'width': 850,
        'height': 200,
        'filebrowserWindowWidth': 975,
        'filebrowserWindowHeight': 550,
    },
}

EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = EMAIL_SERVER_HOST
EMAIL_HOST_USER = EMAIL_USER
EMAIL_HOST_PASSWORD = EMAIL_PASSWORD
EMAIL_PORT = 587

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

LOGIN_URL = '/accounts/register/'

AUTH_USER_MODEL = 'accounts.User'

DATE_INPUT_FORMATS = ['%Y-%m-%d',
                      '%d-%m-%Y',
                      '%d-%m-%y',
                      '%m-%d-%y',
                      '%m-%d-%Y',
                      '%Y-%m-%d',
                      '%d/%m/%Y',
                      '%d/%m/%y',
                      '%m/%d/%Y',
                      '%m/%d/%y',
    ]

AUTHENTICATION_BACKENDS = (
   'social.backends.facebook.FacebookOAuth2',
 'social_core.backends.open_id.OpenIdAuth',
 'social_core.backends.google.GoogleOpenId',
 'social_core.backends.google.GoogleOAuth2',
   'social.backends.twitter.TwitterOAuth',
    'django.contrib.auth.backends.ModelBackend',
    'accounts.backends.LoginUsingEmailBackend',
)

SOCIAL_AUTH_FACEBOOK_KEY = ''
SOCIAL_AUTH_FACEBOOK_SECRET = ''


SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = ''
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = ''

SOCIAL_AUTH_TWITTER_KEY = ''
SOCIAL_AUTH_TWITTER_SECRET = ''

SOCIAL_AUTH_URL_NAMESPACE = 'social'

SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    'social.pipeline.user.create_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.debug.debug',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details',
    'social.pipeline.debug.debug',
)

SOCIAL_AUTH_GOOGLE_OAUTH2_IGNORE_DEFAULT_SCOPE = True
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
'https://www.googleapis.com/auth/userinfo.email',
'https://www.googleapis.com/auth/userinfo.profile'
]


SOCIAL_AUTH_GOOGLE_PLUS_IGNORE_DEFAULT_SCOPE = True
SOCIAL_AUTH_GOOGLE_PLUS_SCOPE = [
'https://www.googleapis.com/auth/plus.login',
'https://www.googleapis.com/auth/userinfo.email',
'https://www.googleapis.com/auth/userinfo.profile'
]

SOCIAL_AUTH_LOGIN_ERROR_URL = '/'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/'
SOCIAL_AUTH_RAISE_EXCEPTIONS = False

BRAINTREE_PRODUCTION = False
BRAINTREE_MERCHANT_ID = ''
BRAINTREE_PUBLIC_KEY = ''
BRAINTREE_PRIVATE_KEY = ''

LOGOUT_REDIRECT_URL = '/'
LOGIN_REDIRECT_URL = '/'


CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("localhost", 6379)],
        },
    },
}

ASGI_APPLICATION = "Project.routing.application"

NOTIFY_USERS_ON_ENTER_OR_LEAVE_ROOMS = True

MSG_TYPE_MESSAGE = 0  
MSG_TYPE_WARNING = 1  
MSG_TYPE_ALERT = 2 
MSG_TYPE_MUTED = 3 
MSG_TYPE_ENTER = 4  
MSG_TYPE_LEAVE = 5 

MESSAGE_TYPES_CHOICES = (
    (MSG_TYPE_MESSAGE, 'MESSAGE'),
    (MSG_TYPE_WARNING, 'WARNING'),
    (MSG_TYPE_ALERT, 'ALERT'),
    (MSG_TYPE_MUTED, 'MUTED'),
    (MSG_TYPE_ENTER, 'ENTER'),
    (MSG_TYPE_LEAVE, 'LEAVE'),
)

MESSAGE_TYPES_LIST = [
    MSG_TYPE_MESSAGE,
    MSG_TYPE_WARNING,
    MSG_TYPE_ALERT,
    MSG_TYPE_MUTED,
    MSG_TYPE_ENTER,
    MSG_TYPE_LEAVE,
]


BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_SEND_EVENTS = False
CELERY_ENABLE_UTC = True
CELERY_ALWAYS_EAGER = True
CELERY_IMPORTS = ("frontend.tasks",)
