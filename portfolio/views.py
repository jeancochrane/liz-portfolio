from django.http import Http404
from django.shortcuts import render
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.files.images import get_image_dimensions

from portfolio.models import Category, Project, About, Contact, Work, Exhibitions


def home(request):
    context = {
        'featured_projects': {}
    }

    # query projects for the featured section
    try:
        featured_projects = Project.objects.filter(featured=True).order_by('-created_date')
    except Project.DoesNotExist:
        raise Http404("""No featured projects found.
                         Select a project to feature on the admin page.""")

    context['featured_projects'] = featured_projects

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
    context = {
        'page': {
            'title': ''
        },
        'project': {},
        'works': {},
        'dimensions': {}
    }

    # Get the project object from the DB
    try:
        project = Project.objects.get(slug=prj)
        context['project'] = project
        context['page']['title'] = project.title
    except Project.DoesNotExist:
        raise Http404("No projects found with the slug '%s'" % prj)

    # Query DB for works corresponding to $project
    try:
        works = Work.objects.filter(parent_project=project).order_by('order')
        # get dimensions of images
        for work in works:
            work.width, work.height = get_image_dimensions(work.work_image.file)
        context['works'] = works

    except Work.DoesNotExist:
        raise Http404("No works found in the project '%s'" % prj)

    return render(request, 'work.html', context)
