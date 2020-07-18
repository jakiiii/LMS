from django.db import models

from django.urls import reverse
from django.db.models.signals import pre_save

from instructor.models.professor import Instructor

from lms.utils import unique_slug_generator


class CertificationQuerySet(models.QuerySet):
    pass


class CertificationManager(models.Manager):
    pass


class Certification(models.Model):
    professor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    title = models.CharField(max_length=250, null=True, blank=True)
    certification_description = models.TextField(max_length=500, null=True, blank=True)
    period = models.DateField(auto_now_add=False, null=True, blank=True)
    ex_end_period = models.DateField(auto_now_add=False, null=True, blank=True)
    slug = models.SlugField(blank=True, unique=True)

    objects = CertificationManager()

    def __str__(self):
        return self.title

    def get_absolute_certification_update_url(self):
        return reverse("certification-update", kwargs={"slug": self.slug})

    def get_absolute_certification_delete_url(self):
        return reverse("certification-delete", kwargs={"slug": self.slug})


def certification_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(certification_pre_save_receiver, sender=Certification)
