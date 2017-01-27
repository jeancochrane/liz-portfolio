from django.http import Http404
from django.shortcuts import render
from django.conf import settings
from django.contrib.sites.models import Site

from portfolio.models import Category, Project, About, Contact, Work, Exhibitions


def home(request):
    context = {
        'projects': {}
    }

    # query projects for the featured section
    try:
        featured_projects = Project.objects.filter(featured=True).order_by('-created_date')
    except Project.DoesNotExist:
        raise Http404("""No featured projects found.
                         Select a project to feature on the admin page.""")

    context['featured_projects'] = featured_projects

    # query projects for the sidebar categories
    sidebar_categories = [category for category in Category.objects.all()]
    print(sidebar_categories)
    # sidebar_categories = ['design', 'zines', 'bodies', 'screens']

    for category in sidebar_categories:
        try:
            context['projects'][category.slug] = Project.objects.filter(category=category).order_by('-created_date')
        except Project.DoesNotExist:
            continue

    return render(request, 'index.html', context)


def about(request):
    context = {
        'page': {
            'title': 'About'
        }
    }
    about = About.objects.last()

    context["bio"] = about.bio

    # media file for development
    context["featured_image"] = about.featured_image

    return render(request, 'about.html', context)


def contact(request):
    context = {
        'page': {
            'title': 'Contact'
        }
    }
    contact = Contact.objects.last()

    if contact.featured_image:
        context["featured_image"] = contact.featured_image

    context["text"] = contact.text

    return render(request, 'contact.html', context)


def exhibitions(request):
    context = {
        'page': {
            'title': 'Exhibitions'
        }
    }
    exhibitions = Exhibitions.objects.last()

    if exhibitions.featured_image:
        context["featured_image"] = exhibitions.featured_image

    context["text"] = exhibitions.text

    return render(request, 'exhibitions.html', context)


def work(request, prj):
    # Get the appropriate project object from the DB
    try:
        project = Project.objects.get(slug=prj)
    except Project.DoesNotExist:
        raise Http404("No projects found with the slug '%s'" % prj)

    # Query DB for works corresponding to $project
    try:
        works = Work.objects.filter(project=project)
        context['works'] = works

    except Work.DoesNotExist:
        raise Http404("No works found in the project '%s'" % prj)

    context = {
        'page': {
            'title': category_obj.name
        },
        'category': category_obj
    }

    return render(request, 'work.html', context)
