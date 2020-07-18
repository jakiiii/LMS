from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils import timezone
from django.db.models.signals import pre_save

from courses.models import Courses, Lessons
from instructor.models import Instructor

from lms.utils import unique_slug_generator
from lms.utils_file import upload_image_path


# Episode QuerySet
class EpisodeQuerySet(models.QuerySet):
    def active(self):
        return self.filter(active=True)

    def is_locked(self):
        return self.filter(locked=True)

    def search(self, query):
        lookup = (
                Q(title__icontains=query) |
                Q(title__iexact=query)
        )
        return self.filter(lookup).distinct()


# Lessons manager
class EpisodeManager(models.Manager):
    def all(self):
        return self.get_queryset().active()

    def is_locked(self):
        return self.get_queryset().is_locked()

    def get_queryset(self):
        return EpisodeQuerySet(self.model, using=self._db)

    def search(self, query):
        return self.get_queryset().search(query)


# Lessons model
class Episode(models.Model):
    episode_instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    lesson_of = models.ForeignKey(Courses, on_delete=models.CASCADE, related_name='episode_lesson')
    series_of = models.ForeignKey(Lessons, on_delete=models.CASCADE, related_name='episode_series')
    title = models.CharField(max_length=150, blank=False, null=False)
    video = models.FileField(upload_to=upload_image_path)
    duration = models.CharField('Duration', max_length=10)
    price = models.DecimalField(max_digits=20, decimal_places=2, null=False, blank=False)
    active = models.BooleanField(default=True)
    locked = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=timezone.now)
    update_time = models.DateTimeField(auto_now=timezone.now)
    slug = models.SlugField(blank=True, unique=True)

    objects = EpisodeManager()

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Episodes'
        verbose_name_plural = 'Episodes'

    def __str__(self):
        return '{}'.format(self.title)

    def get_absolute_episode_url(self):
        return reverse('episode-video', kwargs={"slug": self.slug})

    def get_absolute_update_episode_url(self):
        return reverse('update-episode', kwargs={"slug": self.slug})

    def get_absolute_delete_episode_url(self):
        return reverse("delete-episode", kwargs={"slug": self.slug})


def episode_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(episode_pre_save_receiver, sender=Episode)
