"""gunicorn WSGI server configuration."""

# Based on https://github.com/rdegges/django-skel/blob/master/gunicorn.py.ini.

import os
from multiprocessing import cpu_count


def max_workers():
    return cpu_count()

bind = '0.0.0.0:' + os.environ.get('PORT', '8000')
max_requests = 1000
worker_class = 'gevent'
workers = max_workers()
