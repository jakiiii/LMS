from django.utils import timezone
from django.db import models
from django.urls import reverse
from django.conf import settings
from django.db.models.signals import pre_save

from instructor.models import Instructor

from lms.utils import unique_slug_generator

User = settings.AUTH_USER_MODEL
Student = settings.AUTH_USER_MODEL


class MessageBoxManager(models.Model):
    pass


# Create your models here.
class MessageBox(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    professor = models.OneToOneField(Instructor, on_delete=models.CASCADE, null=True, blank=True)
    # student = models.OneToOneField(Student, on_delete=models.CASCADE, null=True, blank=True)
    subject = models.CharField(max_length=250)
    body = models.TextField()
    datetime = models.DateTimeField(auto_now_add=timezone.now)
    update = models.DateTimeField(auto_now=timezone.now)
    slug = models.SlugField(unique=True, blank=True)

    objects = MessageBoxManager()

    class Meta:
        ordering = ['-datetime']
        verbose_name = 'Message'
        verbose_name_plural = 'Message'

    def __str__(self):
        return self.subject

    @property
    def title(self):
        return self.subject

    def get_absolute_url(self):
        return reverse('admin-detail-message', kwargs={"slug": self.slug})

    def get_absolute_message_delete_url(self):
        return reverse('delete-message', kwargs={"slug": self.slug})

    def get_student_absolute_url(self):
        return reverse('student-detail-message', kwargs={"slug": self.slug})

    def get_student_absolute__delete_url(self):
        return reverse('student-delete-message', kwargs={"slug": self.slug})


def message_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(message_pre_save_receiver, sender=MessageBox)
