"""
Django settings for affiliate project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'aw5o=op#myqi##ma0brwv9ulo$e&bb!1i-j1_e)6*k36c2wjll'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
  'django.contrib.auth',
  'django.contrib.contenttypes',
  'django.contrib.staticfiles',
  'rest_framework',
  'rest_framework.authtoken',
  'captcha',
  'affiliate',
)

MIDDLEWARE_CLASSES = (
  'django.middleware.common.CommonMiddleware',
  'django.middleware.csrf.CsrfViewMiddleware',
  'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'affiliate.urls'

WSGI_APPLICATION = 'affiliate.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'affiliate',
    'USER': 'affiliate',
    'PASSWORD': '123456',
    'HOST': '127.0.0.1',
  }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'th-th'

TIME_ZONE = 'Asia/Bangkok'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

AUTH_USER_MODEL = 'affiliate.User'

REST_FRAMEWORK = {
  'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
  'PAGE_SIZE': 50,
}

CAPTCHA_IMAGE_SIZE = (80, 26)

CAPTCHA_FONT_SIZE = 20

CAPTCHA_LETTER_ROTATION = None

CAPTCHA_BACKGROUND_COLOR = '#eeeeee'

CAPTCHA_CHALLENGE_FUNCT = 'captcha.helpers.math_challenge'

CAPTCHA_NOISE_FUNCTIONS = ()

CAPTCHA_TEXT_FIELD_TEMPLATE = os.path.join(BASE_DIR, 'affiliate/templates/captcha/text_field.html')

CAPTCHA_FIELD_TEMPLATE = os.path.join(BASE_DIR, 'affiliate/templates/captcha/field.html')

import decimal
import sys
AFFILIATE_PERCENT = (
  (1, 100000, decimal.Decimal('0.28')),
  (100001, 1500000, decimal.Decimal('0.35')),
  (1500001, 3200000, decimal.Decimal('0.40')),
  (3200001, sys.maxint, decimal.Decimal('0.45')),
)