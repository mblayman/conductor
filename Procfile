web: gunicorn --config .gunicorn.py config.wsgi:application
worker: celery worker --app conductor:celeryapp --loglevel info
frontend: make frontend
