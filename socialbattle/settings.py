"""
Django settings for socialbattle project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'elsv&hoox@mko0(27^m^z=_14ph$49s@a^&rl5jxkly-va5cjj'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'socialbattle.api',
    'rest_framework',
    'corsheaders',
    'provider',
    'provider.oauth2',
    #'djangular',
    #'announce',
    #'django_facebook',
)

MIDDLEWARE_CLASSES = (
    #'announce.middleware.AnnounceCookieMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
)

ROOT_URLCONF = 'socialbattle.urls'

WSGI_APPLICATION = 'socialbattle.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'socialbattle',
        'HOST': 'localhost',
        'PORT': 3306,
        'USER': 'py',
        'PASSWORD': 'py'
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

MEDIA_ROOT = '/media/'
STATIC_URL = '/static/'
#STATICFILES_DIRS = (os.path.join(BASE_DIR, '/socialbattle/apps/site/'),)
#STATICFILES_DIRS = (BASE_DIR + '/socialbattle/apps/site/',)
#TEMPLATE_DIRS = (os.path.join(BASE_DIR, '/socialbattle/apps/site/html'), )
#TEMPLATE_DIRS = (BASE_DIR + '/socialbattle/apps/site/html', )

REST_FRAMEWORK = {
    # Use hyperlinked styles by default.
    # Only used if the `serializer_class` attribute is not set on a view.
    'DEFAULT_MODEL_SERIALIZER_CLASS':
        'rest_framework.serializers.HyperlinkedModelSerializer',

    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        #'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],

    'DEFAULT_AUTHENTICATION_CLASSES': (
        #'rest_framework.authentication.OAuth2Authentication',
    ), 

    #'PAGINATE_BY': 10
}

AUTH_USER_MODEL = 'api.User'

CORS_ORIGIN_ALLOW_ALL = True
#CORS_URLS_REGEX = r'^api/.*$'

#ANNOUNCE_CLIENT_ADDR = 'localhost:5500'
#ANNOUNCE_API_ADDR = 'localhost:6600'
#ANNOUNCE_HTTPS = False

#FACEBOOK_APP_ID = '1441968896050367'
#FACEBOOK_APP_SECRET = '440e8e4c365b8e2d0e87bb5c42a1e464'