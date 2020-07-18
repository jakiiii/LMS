from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.urls import reverse
from django.db.models.signals import pre_save

from lms.utils import unique_slug_generator

from courses.models import Courses
from instructor.models import Instructor


# Lessons QuerySet
class LessonsQuerySet(models.QuerySet):
    def active(self):
        return self.filter(active=True)

    def search(self, query):
        lookup = (
                Q(lesson_title__icontains=query) |
                Q(lesson_title__iexact=query)
        )
        return self.filter(lookup).distinct()


# Lessons manager
class LessonsManager(models.Manager):
    def get_queryset(self):
        return LessonsQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

    def search(self, query):
        return self.get_queryset().search(query)


# Lessons model
class Lessons(models.Model):
    # course_instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, null=True, blank=True)
    course_of = models.ForeignKey(Courses, on_delete=models.CASCADE, related_name='course_lesson')
    lesson_title = models.CharField('Lessons title', max_length=200, blank=True, null=True)
    price = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    description = models.TextField(max_length=800, null=True, blank=True)
    # lessons_video = models.URLField(max_length=250)
    # lessons_video_duration = models.CharField('Duration', max_length=20, blank=True, null=True)
    lesson_file = models.FileField(upload_to='', null=True, blank=True)
    # lesson_price = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=timezone.now)
    update_time = models.DateTimeField(auto_now=timezone.now)
    slug = models.SlugField(blank=True, unique=True)

    objects = LessonsManager()

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return '{}'.format(self.lesson_title)

    @property
    def title(self):
        return self.lesson_title

    def get_absolute_update_series_url(self):
        return reverse('update-series', kwargs={"slug": self.slug})

    def get_absolute_delete_series_url(self):
        return reverse("delete-lesson", kwargs={"slug": self.slug})


def series_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(series_pre_save_receiver, sender=Lessons)
