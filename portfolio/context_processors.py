from django.conf import settings

from portfolio.models import Category, Project, Exhibitions, Contact


def universal_context(request):
    context = {
        'SITE_NAME': settings.SITE_NAME,
        'SITE_DESCRIPTION': settings.SITE_DESCRIPTION,
        'projects': {}
    }
    context['sidebar_projects'] = Project.objects.all()

    # check to see if Exhibitions/Contact objects exist
    try:
        context['exhibitions'] = Exhibitions.objects.last()
    except Exhibitions.DoesNotExist:
        pass

    try:
        context['contact'] = Contact.objects.last()
    except Contact.DoesNotExist:
        pass

    # Load projects for the sidebar
    sidebar_categories = [category for category in Category.objects.all()]

    for category in sidebar_categories:
        try:
            context['projects'][category.slug] = Project.objects.filter(
                category=category).order_by('order')
        except Project.DoesNotExist:
            continue

    return context
