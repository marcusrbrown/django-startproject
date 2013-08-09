web: newrelic-admin run-program python manage.py run_gunicorn -c gunicorn.py
scheduler: newrelic-admin run-program python manage.py celery worker -B -E --loglevel=INFO --maxtasksperchild=1000
worker: python manage.py celery worker -E --loglevel=INFO --maxtasksperchild=1000
