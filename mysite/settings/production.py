from .base import *
import os
from dotenv import load_dotenv

load_dotenv()
DEBUG = False

# ManifestStaticFilesStorage is recommended in production, to prevent
# outdated JavaScript / CSS assets being served from cache
# (e.g. after a Wagtail upgrade).
# See https://docs.djangoproject.com/en/5.2/ref/contrib/staticfiles/#manifeststaticfilesstorage
STORAGES["staticfiles"]["BACKEND"] = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"

SECRET_KEY=os.getenv('SECRET_KEY')
ALLOWED_HOSTS=['localhost', '206.189.140.88', 'naftaliholland.me']

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

DATABASES = {
    "default": {
		'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'www',
        'USER': 'wwwuser',
        'PASSWORD': 'wwwuser@10503',
        'HOST': 'localhost',
        'PORT': '',
    }
}

try:
    from .local import *
except ImportError:
    pass
