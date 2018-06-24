import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_DIR = os.path.dirname(BASE_DIR)

SECRET_KEY = os.environ['SECRET_KEY']

# Other settings must explicitly opt-in for debug mode.
DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['POSTGRES_DB'],
        'USER': os.environ['POSTGRES_USER'],
        'PASSWORD': os.environ['POSTGRES_PASSWORD'],
        'HOST': '127.0.0.1',
    }
}

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'anymail',
    'corsheaders',
    'localflavor',
    'accounts.apps.AccountsConfig',
    'planner.apps.PlannerConfig',
    'support.apps.SupportConfig',
    'vendor.apps.VendorConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'rollbar.contrib.django.middleware.RollbarNotifierMiddleware',
]

ROOT_URLCONF = 'conductor.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(ROOT_DIR, 'templates'),
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

WSGI_APPLICATION = 'conductor.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',  # noqa
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',  # noqa
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',  # noqa
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',  # noqa
    },
]

CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SESSION_COOKIE_SECURE = True
X_FRAME_OPTIONS = 'DENY'

AUTH_USER_MODEL = 'accounts.User'
LOGIN_REDIRECT_URL = '/app/'
LOGOUT_REDIRECT_URL = '/accounts/login/'

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_ROOT = os.environ['STATIC_ROOT']
STATIC_URL = os.environ['STATIC_URL']
STATICFILES_DIRS = [
    os.path.join(ROOT_DIR, 'assets'),
]
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'  # noqa

CELERY_BROKER_URL = 'amqp://{}:{}@localhost:5672/{}'.format(
    os.environ['RABBITMQ_USER'],
    os.environ['RABBITMQ_PASSWORD'],
    os.environ['RABBITMQ_VHOST']
)

CORS_ORIGIN_WHITELIST = (
    os.environ['CORS_ORIGIN_WHITELIST'],
)

ROLLBAR = {
    'access_token': os.environ['ROLLBAR_ACCESS_TOKEN'],
    'environment': os.environ['ROLLBAR_ENVIRONMENT'],
    'root': BASE_DIR,
    'enabled': bool(os.environ.get('ROLLBAR_ENABLED', False)),
}

CONDUCTOR_EMAIL = os.environ['CONDUCTOR_EMAIL']
EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'
DEFAULT_FROM_EMAIL = '"College Conductor" <noreply@mail.collegeconductor.com>'
ANYMAIL = {
    'MAILGUN_API_KEY': os.environ['MAILGUN_API_KEY'],
}

STRIPE_PUBLISHABLE_KEY = os.environ['STRIPE_PUBLISHABLE_KEY']
