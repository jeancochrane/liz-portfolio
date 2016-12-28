from django.db import models
from django.utils import timezone
from django.contrib.sites.models import Site


class About(models.Model):
    """
    Model to represent Liz's about page.
    """
    name = "About"
    site = models.OneToOneField(Site)  # Can only be one
    featured_image = models.FileField(
        upload_to='about/'
    )
    bio = models.TextField()

    def __str__(self):
        return self.name


class Category(models.Model):
    """
    Model to represent a category of artwork in the DB.
    """
    name = models.CharField(max_length=250)

    # `slug` defines the text that will represent the category in a URL path.
    # Should be short, lowercase, and contain no spaces.
    slug = models.SlugField()

    def __str__(self):
        return self.name


def filepath(instance, filename):
    """
    Callable that returns a filepath for an uploaded image.
    """
    # file will be uploaded to MEDIA_ROOT/<category>/<filename>
    return '{0}/{1}'.format(instance.category.slug, filename)


class Work(models.Model):
    """
    Model to represent an artwork in the DB.
    """
    title = models.CharField(max_length=250)
    materials = models.CharField(max_length=250)
    year = models.IntegerField()
    statement = models.TextField(
        blank=True
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.CASCADE
    )
    created_date = models.DateTimeField(default=timezone.now)
    media_file = models.FileField(
        upload_to=filepath,
        verbose_name='Upload a file'
    )

    def __str__(self):
        return self.title
