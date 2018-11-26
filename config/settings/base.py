import os
from typing import List

from celery.schedules import crontab

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_DIR = os.path.dirname(BASE_DIR)

SECRET_KEY = "y$l*8=9d0b^nbf4c#vs+z=d)vb(3rsgvcx!+2as@f5f2s*#x=q"

# Other settings must explicitly opt-in for debug mode.
DEBUG = False

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "conductor",
        "USER": "conductor",
        "PASSWORD": "conductor",
        "HOST": "127.0.0.1",
    }
}

ALLOWED_HOSTS: List[str] = []

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
    "anymail",
    "localflavor",
    "storages",
    "conductor.accounts.apps.AccountsConfig",
    "conductor.planner.apps.PlannerConfig",
    "conductor.support.apps.SupportConfig",
    "conductor.trackers.apps.TrackersConfig",
    "conductor.vendor.apps.VendorConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "rollbar.contrib.django.middleware.RollbarNotifierMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(ROOT_DIR, "conductor", "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "config.wsgi.application"

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"  # noqa
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SESSION_COOKIE_SECURE = True
X_FRAME_OPTIONS = "DENY"

AUTH_USER_MODEL = "accounts.User"
LOGIN_REDIRECT_URL = "/app/"
LOGOUT_REDIRECT_URL = "/accounts/login/"

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_ROOT = "static"
STATIC_URL = "/static/"
STATICFILES_DIRS = [os.path.join(ROOT_DIR, "assets")]
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"

MEDIA_ROOT = "media"
MEDIA_URL = "/media/"

# The Sites framework is overkill. Set protocol+domain so Celery can make full links.
DOMAIN = ""

CELERY_BROKER_URL = "amqp://conductor:conductor@localhost:5672/conductor"
CELERY_BEAT_SCHEDULE = {
    "common-app-scan": {
        "task": "conductor.trackers.tasks.scan_common_app_schools",
        "schedule": crontab(day_of_week=0, hour=2, minute=0),
    }
}

ROLLBAR = {
    "access_token": "rollbar_access_token",
    "environment": "development",
    "root": BASE_DIR,
    "enabled": False,
}

CONDUCTOR_EMAIL = "matt@conductor.test"
EMAIL_BACKEND = "django.core.mail.backends.dummy.EmailBackend"
DEFAULT_FROM_EMAIL = '"College Conductor" <noreply@mail.collegeconductor.com>'
ANYMAIL = {"MAILGUN_API_KEY": "mailgun_api_key"}

STRIPE_API_KEY = "sk_test_fake_key"
STRIPE_PUBLISHABLE_KEY = "pk_test_fake_key"
STRIPE_PLAN = "fake-plan"

GOOGLE_CLIENT_CONFIG = {
    "web": {
        "project_id": "",
        "client_id": "",
        "client_secret": "",
        "redirect_uris": [""],
        "auth_uri": "https://testserver",
        "token_uri": "",
    }
}

# Override development settings with a secrets file.
try:
    from ._secrets import *  # noqa
except ImportError:
    pass
