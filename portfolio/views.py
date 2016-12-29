from django.http import Http404
from django.shortcuts import render
from django.conf import settings
from django.contrib.sites.models import Site

from portfolio.models import Category, Work, About


def home(request):
    context = {}

    try:
        works = Work.objects.filter(featured=True).order_by('-created_date')
    except Work.DoesNotExist:
        raise Http404("""No featured artworks found.
                         Select an artwork to feature on the admin page.""")

    context['works'] = works
    return render(request, 'index.html', context)


def about(request):
    context = {
        'page': {
            'title': 'About'
        }
    }
    info = About.objects.last()

    context["bio"] = info.bio

    # media file for development
    context["featured_image"] = info.featured_image

    return render(request, 'about.html', context)

def contact(request):
    context = {
        'page': {
            'title': 'Contact'
        }
    }

    return render(request, 'contact.html', context)

def work(request, category):
    # Get the appropriate category object from the DB
    try:
        category_obj = Category.objects.get(slug=category)
    except Category.DoesNotExist:
        raise Http404("No categories found with the slug '%s'" % category)

    context = {
        'page': {
            'title': category_obj.name
        },
        'category': category_obj
    }

    # Query DB for works corresponding to $category
    try:
        works = Work.objects.filter(category=category_obj).order_by('order')
        context['works'] = works
    except Work.DoesNotExist:
        raise Http404("No works found in the category '%s'" % category)

    return render(request, 'work.html', context)
