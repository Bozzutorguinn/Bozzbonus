"""
Django settings for Project project.

Generated by 'django-admin startproject' using Django 1.8.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

#check whether being run on local dev or production
from sys import platform as _platform
if _platform == "linux" or _platform == "linux2":
	system_type = "prod_linux"
elif _platform == "darwin":
	system_type = "dev_mac"
elif _platform == "win32":
	system_type = "dev_windows"



# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'dpfj-7i139ty2u!&)9ogkgd0dgvt)ny@6e##n)+f0pi45)(#q)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

if system_type == 'dev_mac':
    LOGIN_URL = '/user_access/login/'
if system_type == 'prod_linux':
    LOGIN_URL = '/Project/user_access/login/'

LOGIN_REDIRECT_URL = '/property/property/'


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'property',
    'user_access',
    'employees',
    'submittal',
    'submittal_employees',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'Project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

if system_type == "prod_linux":
	DATABASES = {
    	'default': {
        	'ENGINE': 'django.db.backends.postgresql_psycopg2',
        	'NAME': 'djangostack',
        	'HOST': '/opt/bitnami/postgresql',
        	'PORT': '5432',
        	'USER': 'postgres',
        	'PASSWORD': 'bitnami'
    		}	
	}

if system_type == "dev_mac":
	DATABASES = {
		'default': {
			'ENGINE': 'django.db.backends.postgresql_psycopg2',
			'NAME': 'bonus_app',
			'HOST': '127.0.0.1',
			'PORT': '5432',
			'USER': 'mtbarry'
		}
	}


EXAMPLE_DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/Project/static/'
