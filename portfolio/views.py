from django.http import Http404
from django.shortcuts import render
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.files.images import get_image_dimensions

from portfolio.models import Category, Project, About, Contact, Work, Exhibitions


def calculate_dimensions(work):
    """
    Calculates the image widths of a Work object.
    """
    work.image.width, work.image.height = get_image_dimensions(work.image.file)
    work.small.width, work.small.height = get_image_dimensions(work.small.file)
    work.thumbnail.width, work.thumbnail.height = get_image_dimensions(work.thumbnail.file)
    work.medium.width, work.medium.height = get_image_dimensions(work.medium.file)
    work.large.width, work.large.height = get_image_dimensions(work.large.file)

    return work

def home(request):
    context = {
        'featured_projects': {}
    }

    # query projects for the featured section
    try:
        featured_projects = Project.objects.filter(featured=True).order_by('-created_date')
        for project in featured_projects:
            try:
                project.featured_image = calculate_dimensions(project.featured_image)
            except (AttributeError, ValueError):
                pass
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


def custom_server_error(request):
    return render(request, '500.html')


def custom_page_not_found(request):
    return render(request, '404.html')


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
        try:
            project.featured_image = calculate_dimensions(project.featured_image)
        except (AttributeError, ValueError):
            pass
        context['project'] = project
        context['page']['title'] = project.title
    except Project.DoesNotExist:
        raise Http404("No projects found with the slug '%s'" % prj)

    # Query DB for works corresponding to $project
    try:
        works = Work.objects.filter(parent_project=project).order_by('order')
        # get dimensions of images
        for work in works:
            try:
                work = calculate_dimensions(work)
            except (AttributeError, ValueError):  # Handle non-responsives
                work.image.width, work.image.height = get_image_dimensions(work.image.file)
        context['works'] = works

    except Work.DoesNotExist:
        raise Http404("No works found in the project '%s'" % prj)

    return render(request, 'work.html', context)
