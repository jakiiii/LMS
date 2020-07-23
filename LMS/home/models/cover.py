from django.db import models

from category.models import Category

from django.urls import reverse
from django.db.models.signals import pre_save

from lms.utils import unique_slug_generator
from lms.utils_file import upload_image_path


def category_slug():
    category_list = Category.objects.all()
    category = [category.get_absolute_url for category in category_list]
    return category


UrlFor = (
    ('courses_url', 'LESSONS URL'),
    ('register_url', 'SIGNUP URL'),
)


# cover manager
class CoverQuerySet(models.QuerySet):
    pass


# cover manager
class CoverManager(models.Manager):
    pass


# cover model
class Cover(models.Model):
    title = models.CharField(max_length=50, null=True, blank=True)
    image = models.ImageField(upload_to=upload_image_path, default='assets/default_images/no-image.png')
    cover_title_not_authenticated = models.CharField(max_length=50, null=True, blank=True)
    cover_text_not_authenticated = models.TextField(max_length=400, null=True, blank=True)
    url_link_not_authenticated = models.CharField(choices=UrlFor, max_length=25, null=True, blank=True)
    url_btn_not_authenticated = models.CharField(max_length=25, null=True, blank=True)
    cover_title_authenticated = models.CharField(max_length=50, null=True, blank=True)
    cover_text_authenticated = models.TextField(max_length=400, null=True, blank=True)
    url_link_authenticated = models.CharField(choices=UrlFor, max_length=25, null=True, blank=True)
    url_btn_authenticated = models.CharField(max_length=25, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    slug = models.SlugField(blank=True, unique=True)

    objects = CoverManager()

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return self.title

    def get_absolute_update_url(self):
        return reverse("update-slider", kwargs={"slug": self.slug})

    def get_absolute_delete_url(self):
        return reverse("delete-slider", kwargs={"slug": self.slug})


def slider_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(slider_pre_save_receiver, sender=Cover)
