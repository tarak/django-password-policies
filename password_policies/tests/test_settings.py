import os

DEBUG = False

LANGUAGES = (
    ('en', 'English'),
)

LANGUAGE_CODE = 'en'

USE_TZ = False
# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

SECRET_KEY = 'fake-key'

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    "password_policies",
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
        'TEST_NAME': ':memory:',
        'USER': '',
        'PASSWORD': '',
        'PORT': '',
    },
}

ROOT_URLCONF = 'password_policies.tests.urls'

SITE_ID = 1

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), 'templates'),
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'password_policies.middleware.PasswordChangeMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.contrib.messages.context_processors.messages',
    'password_policies.context_processors.password_status',
)

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'
