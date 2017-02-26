from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.sites.models import Site

from portfolio.image_processors import resize, NoThumbnailException


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
        upload_to='about/',
        blank=True
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
        upload_to='exhibitions/',
        blank=True
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
    slug = models.SlugField(
        max_length=250,
        blank=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


def filepath(instance, filename):
    """
    Callable that returns a filepath for an uploaded image.
    """
    # file will be uploaded to MEDIA_ROOT/<category>/<project>/<filename>
    return '{0}/{1}/{2}'.format(instance.parent_project.category.slug,
                                instance.parent_project.slug,
                                filename)


class Project(models.Model):
    """
    Model to represent a project (series of artworks) in the DB.

    Child of Category; parent of Work.
    """
    title = models.CharField(max_length=250)
    # TO DO: Figure out how to remove `slug` from the admin page
    slug = models.SlugField(
        max_length=250,
        blank=True)
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
    order = models.IntegerField(
        verbose_name='position on the sidebar',
        default=1
    )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
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
    image = models.FileField(
        upload_to=filepath,
        verbose_name='upload a file'
    )
    _original_image = None  # Placeholder for checking if image has updated
    thumbnail = models.FileField(
        upload_to=filepath,
        verbose_name='upload a thumbnail (optional)',
        blank=True
    )
    small = models.FileField(
        upload_to=filepath,
        verbose_name='upload a mobile-optimized image (optional)',
        blank=True
    )
    medium = models.FileField(
        upload_to=filepath,
        verbose_name='upload a medium-sized image (optional)',
        blank=True
    )
    large = models.FileField(
        upload_to=filepath,
        verbose_name='upload a large image (optional)',
        blank=True
    )
    order = models.IntegerField(
        verbose_name='position on the category page',
        default=1
    )

    def __str__(self):
        return self.title

    def __init__(self, *args, **kwargs):
        super(Work, self).__init__(*args, **kwargs)
        self._original_image = self.image

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        print('`save` method called for work %s' % self.title)

        # If the admin changes the original image, update all responsive images
        if (self._original_image) and (self.image != self._original_image):
            try:
                self.thumbnail = resize(self.image)
            except NoThumbnailException:
                pass
            try:
                self.small = resize(self.image, img_size="small")
            except NoThumbnailException:
                pass
            try:
                self.medium = resize(self.image, img_size="medium")
            except NoThumbnailException:
                pass
            try:
                self.large = resize(self.image, img_size="large")
            except NoThumbnailException:
                pass

        # If responsive images don't yet exist, make them
        elif not self._original_image:
            if not self.thumbnail:
                try:
                    self.thumbnail = resize(self.image)
                except NoThumbnailException:
                    pass
            if not self.small:
                try:
                    self.small = resize(self.image, img_size="small")
                except NoThumbnailException:
                    pass
            if not self.medium:
                try:
                    self.medium = resize(self.image, img_size="medium")
                except NoThumbnailException:
                    pass
            if not self.large:
                try:
                    self.large = resize(self.image, img_size="large")
                except NoThumbnailException:
                    pass

        self._original_image = self.image
        super(Work, self).save(force_insert, force_update, *args, **kwargs)
