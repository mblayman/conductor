from conductor.settings.base import BASE_DIR


ALLOWED_HOSTS = ['.{{ root_domain }}']

ANYMAIL = {
    'MAILGUN_API_KEY': '{{ secrets.mailgun.api_key }}',
}

CELERY_BROKER_URL = 'amqp://{}:{}@localhost:5672/{}'.format(
    '{{ secrets.rabbitmq.user }}',
    '{{ secrets.rabbitmq.password }}',
    '{{ secrets.rabbitmq.vhost }}',
)

CONDUCTOR_EMAIL = '{{ secrets.conductor.email }}'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '{{ postgres.db }}',
        'USER': '{{ postgres.user }}',
        'PASSWORD': '{{ postgres.password }}',
        'HOST': '127.0.0.1',
    }
}

GOOGLE_CLIENT_CONFIG = {
    'web': {
        'project_id': '{{ secrets.google.project_id }}',
        'client_id': '{{ secrets.google.client_id }}',
        'client_secret': '{{ secrets.google.client_secret }}',
        'redirect_uris': ['{{ secrets.google.redirect_uri }}'],
        'auth_uri': '{{ secrets.google.auth_uri }}',
        'token_uri': '{{ secrets.google.token_uri }}',
        'auth_provider_x509_cert_url': '{{ secrets.google.auth_provider_x509_cert_url }}',
    }
}

ROLLBAR = {
    'access_token': '{{ secrets.rollbar.access_token }}',
    'environment': '{{ deployment }}',
    'root': BASE_DIR,
    'enabled': True,
}

SECRET_KEY = '{{ secrets.conductor.secret_key }}'

STATIC_ROOT = '{{ static_root }}'
STATIC_URL = '{{ static_url }}'

STRIPE_API_KEY = '{{ secrets.stripe.api_key }}'
STRIPE_PUBLISHABLE_KEY = 'secrets.stripe.publishable_key }}'
