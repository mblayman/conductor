import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_DIR = os.path.dirname(BASE_DIR)

SECRET_KEY = 'y$l*8=9d0b^nbf4c#vs+z=d)vb(3rsgvcx!+2as@f5f2s*#x=q'

# Other settings must explicitly opt-in for debug mode.
DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'conductor',
        'USER': 'conductor',
        'PASSWORD': 'conductor',
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
    'localflavor',
    'accounts.apps.AccountsConfig',
    'planner.apps.PlannerConfig',
    'support.apps.SupportConfig',
    'vendor.apps.VendorConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
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

STATIC_ROOT = 'static'
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(ROOT_DIR, 'assets'),
]
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'  # noqa

CELERY_BROKER_URL = 'amqp://conductor:conductor@localhost:5672/conductor'

ROLLBAR = {
    'access_token': 'rollbar_access_token',
    'environment': 'development',
    'root': BASE_DIR,
    'enabled': False,
}

CONDUCTOR_EMAIL = 'matt@conductor.test'
EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'
DEFAULT_FROM_EMAIL = '"College Conductor" <noreply@mail.collegeconductor.com>'
ANYMAIL = {
    'MAILGUN_API_KEY': 'mailgun_api_key',
}

STRIPE_API_KEY = 'sk_test_fake_key'
STRIPE_PUBLISHABLE_KEY = 'pk_test_fake_key'

GOOGLE_CLIENT_CONFIG = {
    'web': {
        'client_id': '',
        'project_id': '',
        'client_secret': '',
        'redirect_uris': [''],
        'auth_uri': 'https://testserver',
        'token_uri': '',
    }
}

# Override development settings with a secrets file.
try:
    from ._secrets import *  # noqa
except ImportError:
    pass
