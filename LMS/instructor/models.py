# from django.db import models
# from django.db.models import Q
# from django.utils import timezone
# from django.conf import settings
#
# from django.urls import reverse
# from django.db.models.signals import pre_save
#
# from lms.utils import unique_slug_generator
# from lms.utils_file import upload_image_path
#
# from ckeditor.fields import RichTextField
#
# User = settings.AUTH_USER_MODEL
#
#
# # Create your QuerySet here.
# class InstructorQuerySet(models.QuerySet):
#     def search(self, query):
#         loopup = (
#             Q(first_name__icontains=query) |
#             Q(last_name__icontains=query) |
#             Q(email__icontains=query) |
#             Q(phone__icontains=query)
#         )
#         return self.filter(loopup).distinct()
#
#
# # Create your models here.
# class InstructorManager(models.Manager):
#     def get_queryset(self):
#         return InstructorQuerySet(self.model, using=self._db)
#
#     def search(self, query):
#         return self.get_queryset().search(query)
#
#
# class Instructor(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     first_name = models.CharField(max_length=100, null=False, blank=False)
#     last_name = models.CharField(max_length=50, null=False, blank=False)
#     short_bio = models.TextField(max_length=400, null=True, blank=True)
#     long_bio = RichTextField()
#     address = RichTextField()
#     email = models.CharField(max_length=40, null=False, blank=False)
#     phone = models.CharField(max_length=20, null=True, blank=True)
#     experience = RichTextField()
#     education = RichTextField()
#     certificate = RichTextField()
#     language = RichTextField()
#     awards = RichTextField()
#     image = models.ImageField(upload_to=upload_image_path, default='assets/images/instructor.png')
#     password = models.CharField(max_length=32, null=True, blank=True)
#     facebook = models.CharField(max_length=150, null=True, blank=True)
#     twitter = models.CharField(max_length=150, null=True, blank=True)
#     linkedin = models.CharField(max_length=150, null=True, blank=True)
#     timestamp = models.DateTimeField(default=timezone.now)
#     slug = models.SlugField(blank=True, unique=True)
#
#     objects = InstructorManager()
#
#     def __str__(self):
#         return '{} {}'.format(self.first_name, self.last_name)
#
#     @property
#     def title(self):
#         return self.last_name
#
#     def get_absolute_url(self):
#         return reverse('professor', kwargs={"slug": self.slug})
#
#     def get_absolute_update_url(self):
#         return reverse("instructor-update", kwargs={"slug": self.slug})
#
#     def get_absolute_delete_url(self):
#         return reverse("professor-delete", kwargs={"slug": self.slug})
#
#
# def instructor_pre_save_receiver(sender, instance, *args, **kwargs):
#     if not instance.slug:
#         instance.slug = unique_slug_generator(instance)
#
#
# pre_save.connect(instructor_pre_save_receiver, sender=Instructor)
