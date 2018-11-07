from config.settings.base import BASE_DIR


ALLOWED_HOSTS = [".{{ root_domain }}"]

ANYMAIL = {"MAILGUN_API_KEY": "{{ secrets.mailgun.api_key }}"}

AWS_ACCESS_KEY_ID = "{{ vault.aws.access_key_id }}"
AWS_SECRET_ACCESS_KEY = "{{ vault.aws.secret_access_key }}"
AWS_S3_REGION_NAME = "{{ vault.aws.region }}"

CELERY_BROKER_URL = "amqp://{}:{}@localhost:5672/{}".format(
    "{{ secrets.rabbitmq.user }}",
    "{{ secrets.rabbitmq.password }}",
    "{{ secrets.rabbitmq.vhost }}",
)

CONDUCTOR_EMAIL = "{{ secrets.conductor.email }}"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "{{ postgres.db }}",
        "USER": "{{ postgres.user }}",
        "PASSWORD": "{{ postgres.password }}",
        "HOST": "127.0.0.1",
    }
}

DOMAIN = "https://{{ client_domain }}"

GOOGLE_CLIENT_CONFIG = {
    "web": {
        "project_id": "{{ secrets.google.project_id }}",
        "client_id": "{{ secrets.google.client_id }}",
        "client_secret": "{{ secrets.google.client_secret }}",
        "redirect_uris": ["{{ secrets.google.redirect_uri }}"],
        "auth_uri": "{{ secrets.google.auth_uri }}",
        "token_uri": "{{ secrets.google.token_uri }}",
        "auth_provider_x509_cert_url": "{{ secrets.google.auth_provider_x509_cert_url }}",  # noqa
    }
}

ROLLBAR = {
    "access_token": "{{ secrets.rollbar.access_token }}",
    "environment": "{{ deployment }}",
    "root": BASE_DIR,
    "enabled": True,
}

SECRET_KEY = "{{ secrets.conductor.secret_key }}"

STATIC_ROOT = "{{ static_root }}"
STATIC_URL = "{{ static_url }}"

STRIPE_API_KEY = "{{ secrets.stripe.api_key }}"
STRIPE_PUBLISHABLE_KEY = "secrets.stripe.publishable_key }}"
STRIPE_PLAN = "{{ secrets.stripe.plan }}"
