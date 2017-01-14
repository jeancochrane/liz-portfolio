from django.conf import settings

from portfolio.models import Category, Project


def universal_context(request):
    context = {
        'SITE_NAME': settings.SITE_NAME,
        'SITE_DESCRIPTION': settings.SITE_DESCRIPTION
    }
    context['sidebar_categories'] = Category.objects.all()
    context['sidebar_projects'] = Project.objects.all()

    return context
