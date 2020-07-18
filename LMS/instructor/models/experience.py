from django.db import models

from django.urls import reverse
from django.db.models.signals import pre_save

from instructor.models.professor import Instructor

from lms.utils import unique_slug_generator


class ExperienceQuerySet(models.QuerySet):
    pass


class ExperienceManager(models.Manager):
    pass


class Experience(models.Model):
    professor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    title = models.CharField(max_length=250, null=True, blank=True)
    experience_description = models.TextField(max_length=500, null=True, blank=True)
    ex_period = models.DateField(auto_now_add=False, null=True, blank=True)
    ex_end_period = models.DateField(auto_now_add=False, null=True, blank=True)
    slug = models.SlugField(blank=True, unique=True)

    objects = ExperienceManager()

    def __str__(self):
        return self.title

    def get_absolute_experience_update_url(self):
        return reverse("experience-update", kwargs={"slug": self.slug})

    def get_absolute_experience_delete_url(self):
        return reverse("experience-delete", kwargs={"slug": self.slug})


def experience_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(experience_pre_save_receiver, sender=Experience)
