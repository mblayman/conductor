api: gunicorn --config .gunicorn.py conductor.wsgi:application
# Somthing is going on with Celery in this new virtualenv on 3.6.5
# so that it won't connect with amqp. Since I'm not using the worker
# for now locally, ignore the issue.
#worker: celery worker --app conductor:celeryapp --loglevel info
frontend: make frontend
