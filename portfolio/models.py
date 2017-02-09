from django.db import models
from django.utils import timezone
from django.utils.text import slugify
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

    class Meta:
        verbose_name_plural = "about page"

    def __str__(self):
        return self.name


class Contact(models.Model):
    """
    Model to represent Liz's contact page.
    """
    name = "Contact"
    site = models.OneToOneField(Site)  # Can only be one
    featured_image = models.FileField(
        upload_to='about/'
    )
    text = models.TextField()

    class Meta:
        verbose_name_plural = "contact page"

    def __str__(self):
        return self.name


class Exhibitions(models.Model):
    """
    Model to represent Liz's exhibitions page.
    """
    name = "Exhibitions"
    site = models.OneToOneField(Site)  # Can only be one
    featured_image = models.FileField(
        upload_to='exhibitions/'
    )
    text = models.TextField()

    class Meta:
        verbose_name_plural = "exhibitions page"

    def __str__(self):
        return self.name


class Category(models.Model):
    """
    Model to represent a category of work in the DB.

    Parent model for uploaded work.
    """
    name = models.CharField(max_length=250)

    # `slug` defines the text that will represent the category in a URL path.
    # Should be short, lowercase, and contain no spaces.
    slug = models.SlugField()

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


def filepath(instance, filename):
    """
    Callable that returns a filepath for an uploaded image.
    """
    # file will be uploaded to MEDIA_ROOT/<category>/<project>/<filename>
    return '{0}/{1}'.format(instance.parent_project.category.slug,
                            instance.parent_project.slug,
                            filename)


class Project(models.Model):
    """
    Model to represent a project (series of artworks) in the DB.

    Child of Category; parent of Work.
    """
    title = models.CharField(max_length=250)
    # TO DO: Figure out how to remove `slug` from the admin page
    slug = models.SlugField()
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
    featured = models.BooleanField(
        default=False,
        verbose_name='feature this project on the home page')
    featured_image = models.ForeignKey(
        'Work',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Project, self).save(*args, **kwargs)


class Work(models.Model):
    """
    Model to represent an artwork in the DB.

    Child of Project.
    """
    title = models.CharField(max_length=250)
    alt_text = models.CharField(max_length=250)
    parent_project = models.ForeignKey(
        'Project',
        on_delete=models.CASCADE
    )
    created_date = models.DateTimeField(default=timezone.now)
    work_image = models.FileField(
        upload_to=filepath,
        verbose_name='upload a file'
    )
    order = models.IntegerField(
        verbose_name='position on the category page',
        default=1
    )
    featured = models.BooleanField(
        default=False,
        verbose_name='feature image on the project page')

    def __str__(self):
        return self.title
