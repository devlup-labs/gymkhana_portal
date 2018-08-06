"""
WSGI config for gymkhana project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os
import sys
from decouple import config

from django.core.wsgi import get_wsgi_application

path = config('APP_SRC', cast=str)
if path not in sys.path:
    sys.path.append(path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gymkhana.settings")

application = get_wsgi_application()
