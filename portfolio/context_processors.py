from django.conf import settings

from portfolio.models import Category, Project


def universal_context(request):
    context = {
        'SITE_NAME': settings.SITE_NAME,
        'SITE_DESCRIPTION': settings.SITE_DESCRIPTION,
        'projects': {}
    }
    context['sidebar_projects'] = Project.objects.all()

    sidebar_categories = [category for category in Category.objects.all()]

    for category in sidebar_categories:
        try:
            context['projects'][category.slug] = Project.objects.filter(category=category).order_by('-created_date')
        except Project.DoesNotExist:
            continue

    return context
