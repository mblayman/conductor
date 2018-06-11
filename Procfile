web: gunicorn --config .gunicorn.py conductor.wsgi:application
worker: celery worker --app conductor:celeryapp --loglevel info
frontend: make frontend
