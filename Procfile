web: gunicorn --config .gunicorn.py conductor.wsgi:application
worker: hupper -m celery worker --app conductor:celeryapp --loglevel info
frontend: make frontend
