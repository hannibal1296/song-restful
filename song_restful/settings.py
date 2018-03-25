import os
from .settings_secret_key import secret_key

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Put your secret key here
SECRET_KEY = secret_key
DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Tools
    'rest_framework',
    'rest_framework.authtoken',
    # 'oauth2_provider',
    # 'social_django',
    # 'rest_framework_social_oauth2',
    'corsheaders',

    # APPs
    'song_restful',
    'song',
    'song_scraper',
    'email_authentication',
    'account',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]

ROOT_URLCONF = 'song_restful.urls'

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
                # 'social_django.context_processors.backends',
                # 'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'song_restful.wsgi.application'

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # }

    'default':{
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'test_db',
        'USER': 'BaeHaneul',
        'PASSWORD': '',
        'HOST': 'localhost',
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

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'ROK'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
AUTH_USER_MODEL = 'account.Account'


# PAGINATION 을 쓰기 위해 별도로 설정해줘야 한다.
REST_FRAMEWORK = {
    # 전역 pagination
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,  # DEFAULT is 3

    # 전체적인 접근량 제어; scope 별로 요청된 timestamp를 list로 유지.
    # 'DEFAULT_THROTTLE_CLASSES': [
    #     'rest_framework.throttling.UserRateThrottle',
    # ],
    # 'DEFAULT_THROTTLE_RATES': {
    #     'user': '5/day',  # format: number/interval  e.g. "10/m"
    # },

    # 각 API별로 서로 다른 Rate 적용하기
    # 'DEFAULT_THROTTLE_CLASSES': [
    #     'rest_framework.throttling.ScopedRateThrottle',  # Instead of .UserRateThrottle
    # ],
    # 'DEFAULT_THROTTLE_RATES': {
    #     'song': '5/m',
    #     'artist': '3/m',
    #     'album': '1/m',
    # }
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        # 'rest_framework.permissions.IsAuthenticated',
    )
}

# To switch from username to email
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False

# FOR TOKEN AUTHENTICATION, Test this (with single quotes and capital letters):
# http GET 127.0.0.1:8000/whatever 'Authorization: Token your_token_value'
# token key: 97eaf278918ce26fd07068c4da9fac8f0be7ec25

# FOR Cross Origin Resource Sharing (CORS)
CORS_ORIGIN_WHITELIST = (
    'localhost:8000',
    'localhost:8001',
    'localhost:9000',
    '127.0.0.1:8000',
    '127.0.0.1:8001',
    '127.0.0.1:9000',
)
CORS_ALLOW_METHODS = (
    'GET',
)

# Rates 제한 메커니즘 설명
'''
1. SingleRateThrottle에서는 요청한 시간의 타임스탬프를 리스트로 유지
2. 매 요청시마다
    1) 캐시에서 타임스탬프 리스트를 가져옴
    2) 체크범위 밖의 타임스탬프 값은 모두 버림
    3) 타임스탬프 리스트의 크기가 허용범위보다 클 경우, 요청을 거부
    4) 타임스탬프 리스트의 크기가 허용범위보다 작은 경우,
        현재 타임스탬프를 타임스탬프 리스트에 추가하고 캐시에 다시 저장
'''
