from django.conf import settings


def expose_settings(request):
    """
    Put things into the context to make them available in templates.
    https://docs.djangoproject.com/en/4.1/ref/templates/api/#using-requestcontext
    """
    return {
        "MATOMO_SITE_ID": settings.MATOMO_SITE_ID,
        "MATOMO_URL": settings.MATOMO_URL,
        "MATOMO_TAG_MANAGER_CONTAINER": settings.MATOMO_TAG_MANAGER_CONTAINER,
    }
