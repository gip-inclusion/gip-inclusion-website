"""
Django settings for gip_inclusion_website project.

Generated by 'django-admin startproject' using Django 3.2.16.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/

Inspiration
https://github.com/betagouv/tous-a-bord/blob/main/config/settings.py
"""

import os
from pathlib import Path

import dj_database_url
from botocore.config import Config
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True if os.getenv("DEBUG") == "True" else False

HOST_URL = os.getenv("HOST_URL", "127.0.0.1, localhost")

ALLOWED_HOSTS = HOST_URL.replace(" ", "").split(",")

# Application definition

INSTALLED_APPS = [
    "storages",
    "wagtail.contrib.redirects",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.admin",
    "wagtail.search",
    "wagtail.snippets",
    "wagtail",
    "wagtail_modeladmin",
    "wagtailmenus",
    "taggit",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    "widget_tweaks",
    "dsfr",
    "sass_processor",
    "markdownify",
    "cms",
    "services",
    "files",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "middleware.multidomain.multidomain_middleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "dsfr/templates"),
            os.path.join(BASE_DIR, "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "dsfr.context_processors.site_config",
                "wagtailmenus.context_processors.wagtailmenus",
                "config.settings_context_processors.expose_settings",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASE_URL = os.getenv("DATABASE_URL")
DATABASES = {
    "default": dj_database_url.parse(
        DATABASE_URL,
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "fr-FR"

TIME_ZONE = "Europe/Paris"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/
STATIC_URL = "static/"
STATIC_ROOT = "staticfiles"
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "sass_processor.finders.CssFinder",
    "django.contrib.staticfiles.finders.FileSystemFinder",
]

# S3 uploads
# ------------------------------------------------------------------------------

AWS_S3_ACCESS_KEY_ID = os.getenv("S3_KEY_ID", "123")
AWS_S3_SECRET_ACCESS_KEY = os.getenv("S3_KEY_SECRET", "secret")
AWS_S3_ENDPOINT_URL = f"{os.getenv('S3_PROTOCOL', 'https')}://{os.getenv('S3_HOST', 'set-var-env.com/')}"
AWS_STORAGE_BUCKET_NAME = os.getenv("S3_BUCKET_NAME", "set-bucket-name")
AWS_S3_STORAGE_BUCKET_REGION = os.getenv("S3_BUCKET_REGION", "fr")
AWS_S3_FILE_OVERWRITE = False
# CleverCloud S3 implementation does not support recent data integrity features from AWS.
# https://github.com/boto/boto3/issues/4392
# https://github.com/boto/boto3/issues/4398#issuecomment-2619946229
AWS_S3_CLIENT_CONFIG = Config(
    request_checksum_calculation="when_required",
    response_checksum_validation="when_required",
)

# MEDIA CONFIGURATION
# ------------------------------------------------------------------------------

# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = f"https://{AWS_S3_ENDPOINT_URL}/"  # noqa

DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

# Django Sass
SASS_PROCESSOR_ROOT = os.path.join(BASE_DIR, "static")

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

MOCK_EXTERNAL_API = os.getenv("MOCK_EXTERNAL_API", "False")

SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_AGE = 60 * 60

# Wagtail settings
# https://docs.wagtail.org/en/stable/reference/settings.html

WAGTAIL_SITE_NAME = "La plateforme de l'inclusion"

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
WAGTAILADMIN_BASE_URL = f"{os.getenv('HOST_PROTO', 'https')}://{HOST_URL[-1]}"

# Disable Gravatar service
WAGTAIL_GRAVATAR_PROVIDER_URL = None

WAGTAIL_RICHTEXT_FIELD_FEATURES = [
    "h2",
    "h3",
    "h4",
    "bold",
    "italic",
    "link",
    "document-link",
    "image",
    "embed",
]

WAGTAILEMBEDS_RESPONSIVE_HTML = False
WAGTAIL_MODERATION_ENABLED = False

WAGTAILMENUS_FLAT_MENUS_HANDLE_CHOICES = (
    ("header_tools", "Menu en haut à droite"),
    ("footer", "Menu en pied de page"),
    ("footer_ressources", "Menu Ressources du pied de page"),
)

WAGTAILEMBEDS_FINDERS = [
    {
        "class": "cms.embeds_finders.GristFinder",
    },
    {
        "class": "cms.embeds_finders.MetabaseFinder",
    },
    # Handles all other oEmbed providers the default way
    {
        "class": "wagtail.embeds.finders.oembed",
    },
]

# Height for custom Grist Embed
WAGTAILEMBEDS_GRIST_HEIGHT = 400

# Height for custom Metabase Embed
WAGTAILEMBEDS_METABASE_HEIGHT = 650

# Auto-sizer script for custom Metabase Embed
WAGTAILEMBEDS_METABASE_IFRAME_RESIZER_URL = "/app/iframeResizer.js"

# Increase throttling to avoid Bad request errors when saving large pages
# https://docs.djangoproject.com/en/4.2/ref/settings/#data-upload-max-number-fields
DATA_UPLOAD_MAX_NUMBER_FIELDS = os.getenv("DATA_UPLOAD_MAX_NUMBER_FIELDS", 10000)

# MATOMO
# ---------------------------------------
MATOMO_SITE_ID = os.getenv("MATOMO_SITE_ID")
MATOMO_URL = os.getenv("MATOMO_URL")
MATOMO_TAG_MANAGER_CONTAINER = os.getenv("MATOMO_TAG_MANAGER_CONTAINER")
