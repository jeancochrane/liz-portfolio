from django.conf import settings


def universal_context(request):
    context = {
        'SITE_NAME': settings.SITE_NAME,
        'SITE_DESCRIPTION': settings.SITE_DESCRIPTION
    }
    return context
