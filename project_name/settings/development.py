"""Settings used in the development environment."""

import dj_database_url

from base import *

## Debug configuration
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
TEMPLATE_DEBUG = DEBUG


## Email configuration
# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


## Database configuration
try:
    DEFAULT_DATABASE_URL = 'postgres://%s@localhost/%s' % (SITE_NAME, SITE_NAME)
except ImportError:
    # Point to a local sqlite3 instance by default.
    DEFAULT_DATABASE_URL = 'sqlite:///%s' % project_path('db.sqlite')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': dj_database_url.config(default=DEFAULT_DATABASE_URL)
}


## Middleware configuration
# See: https://docs.djangoproject.com/en/dev/ref/settings/#middleware-classes
MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)


## Cache configuration
# See: https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES_DEV = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    },
}

if CACHES is None:
    CACHES = dict()
CACHES.update(CACHES_DEV)


## Installed app configuration
# See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS += (
    # django-debug-toolbar
    'debug_toolbar',
)


## Internal IPs configuration
# See: https://docs.djangoproject.com/en/dev/ref/settings/#internal-ips
INTERNAL_IPS = (
    '127.0.0.1',
)


DEBUG_LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'root': {
        'level': 'DEBUG',
        'handlers': ['console'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
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
    },
}

# Augment the existing LOGGING configuration.
if LOGGING is None:
    LOGGING = dict()
LOGGING.update(DEBUG_LOGGING)


## django-celery / celery configuration
# See: http://docs.celeryproject.org/en/latest/configuration.html#celery-always-eager
CELERY_ALWAYS_EAGER = True


## django-debug-toolbar configuration
# See: https://github.com/django-debug-toolbar/django-debug-toolbar
DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}
