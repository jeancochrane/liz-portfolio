from django.http import Http404
from django.shortcuts import render
from django.conf import settings
from django.contrib.sites.models import Site

from portfolio.models import Category, Work, Project, About, Contact


def home(request):
    context = {}

    try:
        projects = Project.objects.filter(featured=True).order_by('-created_date')
    except Work.DoesNotExist:
        raise Http404("""No featured projects found.
                         Select a project to feature on the admin page.""")

    context['work'] = projects
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


def work(request, prj):
    # Get the appropriate category object from the DB
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


def exhibitions(request):
    context = {
        'page': {
            'title': 'Exhibitions'
        }
    }

    # TO DO: define context for exhibition page

    return render(request, 'exhibitions.html', context)
