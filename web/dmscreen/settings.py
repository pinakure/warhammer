import os
DEBUG = True
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = os.environ.get('DJANGO_SECRET')
CSRF_TRUSTED_ORIGINS = [ 'https://warhammer.iskarion.ddns.net', ]
URL_ROOT = 'https://warhammer.iskarion.ddns.net'
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True
SOCIALACCOUNT_LOGIN_ON_GET = True
SITE_ID = 1
ALLOWED_HOSTS = [
    'warhammer.iskarion.ddns.net',
]
INSTALLED_APPS = [
    # Required for KeyCloak
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.openid_connect',
    # ---------------------------
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'dmscreen',
]
MIDDLEWARE = [

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'dmscreen.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
			os.path.join(BASE_DIR, 'templates/common')
        ],
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

WSGI_APPLICATION = 'dmscreen.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),#warhammer
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': '5432',
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

MEDIA_ROOT = (os.path.join(BASE_DIR, 'media'))
MEDIA_URL = '/media/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),) 
STATIC_URL = '/static/'
STATIC_ROOT = '/static/warhammer'

SOCIALACCOUNT_PROVIDERS = {
    'keycloak': {
        'KEYCLOAK_URL': 'http://auth-service:8080', # Dirección de tu máquina Docker
        'ID': 'Warhammer',
        'APP': {
            'client_id': 'warhammer',
            'secret': os.environ.get('KC_SECRET'),
            'key': ''
        }
    }
}
X_FRAME_OPTIONS = 'ALLOW'
