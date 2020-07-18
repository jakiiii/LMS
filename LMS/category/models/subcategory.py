from django.db import models
from django.db.models.signals import pre_save
from django.urls import reverse

from category.models import Category

from ckeditor.fields import RichTextField

from lms.utils import unique_slug_generator
from lms.utils_file import upload_image_path


# Subcategory manager
class SubcategoryManager(models.Manager):
    pass


# subcategory models
class Subcategory(models.Model):
    subcategory = models.CharField('Sub category name', max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory_short_desc = models.TextField(max_length=400, null=True, blank=True)
    subcategory_long_desc = RichTextField()
    what_u_will_learn = RichTextField()
    created_at = models.DateField(auto_now_add=True, blank=True, null=True)
    image = models.ImageField(upload_to=upload_image_path, default='assets/default_images/no-image.png')
    slug = models.SlugField(blank=True, unique=True, null=True)

    def __str__(self):
        return self.subcategory

    @property
    def title(self):
        return self.subcategory

    def get_absolute_url(self):
        return reverse('subcategory', kwargs={"slug": self.slug})


def subcategory_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(subcategory_pre_save_receiver, sender=Subcategory)
