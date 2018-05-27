#!/usr/bin/env python
import os
import sys

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'conductor.settings.development')

    if 'test' in sys.argv:
        # For now, fake setting the environment for testing.
        os.environ['DJANGO_SETTINGS_MODULE'] = 'conductor.settings.test'
        os.environ['CONDUCTOR_EMAIL'] = 'matt@conductor.dev'
        os.environ['CORS_ORIGIN_WHITELIST'] = 'localhost:4200'
        os.environ['MAILGUN_API_KEY'] = 'mailgun'
        os.environ['POSTGRES_DB'] = 'conductor'
        os.environ['POSTGRES_PASSWORD'] = 'conductor'
        os.environ['POSTGRES_USER'] = 'conductor'
        os.environ['RABBITMQ_USER'] = 'conductor'
        os.environ['RABBITMQ_PASSWORD'] = 'conductor'
        os.environ['RABBITMQ_VHOST'] = 'conductor'
        os.environ['ROLLBAR_ACCESS_TOKEN'] = 'rollbar'
        os.environ['ROLLBAR_ENVIRONMENT'] = 'test'
        os.environ['SECRET_KEY'] = 'asecrettoeverybody'
        os.environ['STATIC_ROOT'] = 'static'
        os.environ['STATIC_URL'] = '/static/'
        os.environ['STRIPE_API_KEY'] = 'sk_test_fake_key'
        os.environ['STRIPE_PUBLISHABLE_KEY'] = 'pk_test_fake_key'

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
