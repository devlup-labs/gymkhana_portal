from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'q$o5mx19x9(9_^rzqf@o@s^t%t!ghix7($f9ymy49_^ryzq9x9'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

HTML_MINIFY = False

ALLOWED_HOSTS = ['127.0.0.1']

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, '../db.sqlite3'),
    }
}

INSTALLED_APPS += ['fixture']

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions.
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
    )
}
