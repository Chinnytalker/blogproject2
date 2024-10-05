from .settings import *



DEBUG = False
SECRET_KEY = 'test-secret-key'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}