from .base import *

DEBUG = TEMPLATE_DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'quipy/dev.db',
    }
}

INSTALLED_APPS += [
    'debug_toolbar',
]
