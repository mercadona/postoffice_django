import os

SECRET_KEY = 'psst'

DEBUG = True
USE_TZ = True
ROOT_URLCONF = 'postoffice_django.urls'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postoffice_django',
        'USER': 'postoffice_django',
        'PASSWORD': 'postoffice_django',
        'HOST': os.environ.get('PG_HOST', 'localhost'),
        'PORT': os.environ.get('PG_PORT', '6542')
    },
}

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sites',
    'postoffice_django'
)

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)

POSTOFFICE = {
    'URL': 'http://fake.service',
    'CONSUMERS': [
        {
            'topic': 'some_topic',
            'target': 'http://www.some_url.com',
            'type': 'http',
            'timeout': 20,
            'retry': 60,
            'from_now': True
        },
        {
            'topic': 'another_topic',
            'target': 'http://www.another_url.com',
            'type': 'pubsub',
            'from_now': False
        }],
    'TOPICS': ['topic_to_be_created', 'another_topic_to_be_created'],
    'TIMEOUT': 0.3,
    'BULK_TIMEOUT': 1.2,
    'ORIGIN_HOST': 'example.com'
}
