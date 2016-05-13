#!/usr/bin/env python
import os
import sys

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'conductor.settings.development')

    if 'test' in sys.argv:
        # For now, fake setting the environment for testing.
        os.environ['DJANGO_SETTINGS_MODULE'] = 'conductor.settings.test'
        os.environ['CORS_ORIGIN_WHITELIST'] = 'localhost:4200'
        os.environ['SECRET_KEY'] = 'asecrettoeverybody'
        os.environ['STATIC_URL'] = '/static/'

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
