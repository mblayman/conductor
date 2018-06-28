from conductor.settings.base import BASE_DIR


CONDUCTOR_EMAIL = '{{ secrets.conductor.email }}'

ANYMAIL = {
    'MAILGUN_API_KEY': '{{ secrets.mailgun.api_key }}',
}

CELERY_BROKER_URL = 'amqp://{}:{}@localhost:5672/{}'.format(
    '{{ secrets.rabbitmq.user }}',
    '{{ secrets.rabbitmq.password }}',
    '{{ secrets.rabbitmq.vhost }}',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '{{ postgres.db }}',
        'USER': '{{ postgres.user }}',
        'PASSWORD': '{{ postgres.password }}',
        'HOST': '127.0.0.1',
    }
}

ROLLBAR = {
    'access_token': '{{ secrets.rollbar.acces_token }}',
    'environment': '{{ deployment }}',
    'root': BASE_DIR,
    'enabled': True,
}
