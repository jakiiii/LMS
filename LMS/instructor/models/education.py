from django.db import models

from django.urls import reverse
from django.db.models.signals import pre_save

from instructor.models.professor import Instructor

from lms.utils import unique_slug_generator


class EducationQuerySet(models.QuerySet):
    pass


class EducationManager(models.Manager):
    pass


class Education(models.Model):
    professor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    title = models.CharField(max_length=250, null=True, blank=True)
    Institute_name = models.CharField(max_length=250, null=True, blank=True)
    from_date = models.DateField(auto_now_add=False, null=True, blank=True)
    to_date = models.DateField(auto_now_add=False, null=True, blank=True)
    slug = models.SlugField(blank=True, unique=True)

    objects = EducationManager()

    def __str__(self):
        return self.title

    def get_absolute_education_update_url(self):
        return reverse("education-update", kwargs={"slug": self.slug})

    def get_absolute_education_delete_url(self):
        return reverse("education-delete", kwargs={"slug": self.slug})


def education_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(education_pre_save_receiver, sender=Education)
