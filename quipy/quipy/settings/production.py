from .base import *

import os

DEBUG = TEMPLATE_DEBUG = os.getenv('DJANGO_DEBUG', False)

INSTALLED_APPS += [
    'gunicorn',
]
