SECRET_KEY = 'psst'

DEBUG = True
USE_TZ = True


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postoffice_django',
        'USER': 'postoffice_django',
        'PASSWORD': 'postoffice_django',
        'HOST': 'localhost',
        'PORT': '6543'
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
    'ORIGIN_HOST': 'example.com'
}
