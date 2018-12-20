web: gunicorn --config .gunicorn.py config.wsgi:application
worker: hupper -m celery worker --app conductor:celeryapp --loglevel info
frontend: make frontend
