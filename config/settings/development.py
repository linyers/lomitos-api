from .base import *

SECRET_KEY = os.environ.get('SECRET_KEY') 

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

MEDIA_ROOT = Path.joinpath(BASE_DIR, 'media')
STATIC_ROOT = Path.joinpath(BASE_DIR,'static')