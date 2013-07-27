"""Settings used in the production environment."""

import os

from memcacheify import memcacheify
from postgresify import postgresify
from boto.s3.connection import ProtocolIndependentOrdinaryCallingFormat

from base import *


## Email configuration
# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-host
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-host-password
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-host-user
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'your_email@example.com')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-port
EMAIL_PORT = os.environ.get('EMAIL_PORT', 587)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-subject-prefix
EMAIL_SUBJECT_PREFIX = '[%s] ' % SITE_NAME

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-use-tls
EMAIL_USE_TLS = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#server-email
SERVER_EMAIL = EMAIL_HOST_USER


## Database configuration
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = postgresify()


## Cache configuration
# See: https://docs.djangoproject.com/en/dev/ref/settings/#caches
if CACHES is None:
    CACHES = dict()
CACHES.update(memcacheify())


## Secret key configuration
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Use the value set in the Heroku configuration.
SECRET_KEY = os.environ.get('SECRET_KEY', SECRET_KEY)


## Gunicorn configuration
# See: http://gunicorn.org/run.html
# See: https://docs.djangoproject.com/en/dev/howto/deployment/wsgi/gunicorn/
INSTALLED_APPS += (
    'gunicorn',
)


## django-storages and AWS configuration
# See: http://django-storages.readthedocs.org/en/latest/index.html
# See: http://django-storages.readthedocs.org/en/latest/backends/amazon-S3.html#settings

INSTALLED_APPS += (
    'storages',
)


## Amazon Web Services configuration
# Values are based on the ones found here:
# http://balzerg.blogspot.com/2012/09/staticfiles-on-heroku-with-django.html
AWS_S3_CALLING_FORMAT = ProtocolIndependentOrdinaryCallingFormat()
AWS_QUERYSTRING_AUTH = False


## Static files configuration
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
# Serve static content out of S3.
STATIC_URL = '//s3.amazonaws.com/%s/' % AWS_STORAGE_BUCKET_NAME

# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATICFILES_STORAGE = '%s.storage.S3PipelineStorage' % SITE_NAME

# See: https://docs.djangoproject.com/en/dev/ref/settings/#admin-media-prefix
# Note: This setting is still used in Django 1.4.
ADMIN_MEDIA_PREFIX = STATIC_URL + '/admin/'


## Media configuration
# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
# The media root is located in a subfolder of the S3 bucket.
MEDIA_ROOT = '/media/'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
# The media URL is relative to the static files URL given above.
MEDIA_URL = STATIC_URL + 'media/'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#default-file-storage
DEFAULT_FILE_STORAGE = '%s.storage.MediaS3BotoStorage' % SITE_NAME


## Template configuration
# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
if not DEBUG:
    TEMPLATE_LOADERS = (
        ('django.template.loaders.cached.Loader', (
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        )),
    )


## django-celery / celery configuration
# See: http://docs.celeryproject.org/en/latest/configuration.html#broker-transport
BROKER_TRANSPORT = 'amqplib'

# See: http://docs.celeryproject.org/en/latest/configuration.html#broker-url
BROKER_URL = os.environ.get('RABBITMQ_URL') or os.environ.get('CLOUDAMQP_URL')

# From https://github.com/rdegges/django-skel:
# Set this number to the amount of allowed concurrent connections on your AMQP
# provider, divided by the amount of active workers you have.
#
# For example, if you have the 'Little Lemur' CloudAMQP plan (their free tier),
# they allow 3 concurrent connections. So if you run a single worker, you'd
# want this number to be 3. If you had 3 workers running, you'd lower this
# number to 1, since 3 workers each maintaining one open connection = 3
# connections total.
#
# See: http://docs.celeryproject.org/en/latest/configuration.html#broker-pool-limit
BROKER_POOL_LIMIT = 3

# See: http://docs.celeryproject.org/en/latest/configuration.html#broker-connection-max-retries
BROKER_CONNECTION_MAX_RETRIES = 0

# See: http://docs.celeryproject.org/en/latest/configuration.html#celery-result-backend
CELERY_RESULT_BACKEND = 'amqp'


## Raven / Sentry configuration
# See: https://www.getsentry.com/docs/python/django/
# See: http://raven.readthedocs.org/en/latest/config/django.html
INSTALLED_APPS += (
    'raven.contrib.django',
)

SENTRY_DSN = os.environ.get('SENTRY_DSN')

SENTRY_LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['sentry'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'sentry': {
            'level': 'ERROR',
            'class': 'raven.contrib.django.handlers.SentryHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console', 'sentry'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'celery': {
            'level': 'WARNING',
            'handlers': ['sentry'],
            'propagate': False,
        },
    },
}

# Augment the existing LOGGING configuration.
if LOGGING is None:
    LOGGING = dict()
LOGGING.update(SENTRY_LOGGING)

# The documenation recommend placing Sentry middleware as high as possible.
MIDDLEWARE_CLASSES = (
    'raven.contrib.django.middleware.SentryResponseErrorIdMiddleware',
    'raven.contrib.django.middleware.SentryLogMiddleware',
) + MIDDLEWARE_CLASSES
