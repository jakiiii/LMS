from django.db import models
from django.db.models import Q
from django.conf import settings
from django.utils import timezone
from django.utils.crypto import get_random_string

from django.urls import reverse
from django.db.models.signals import pre_save

from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

from lms.utils import unique_slug_generator

# from accounts.models import User
from category.models import Category, Subcategory

from lms.utils_file import upload_image_path

User = settings.AUTH_USER_MODEL

CourseFor = (
    ('beginner', ' BEGINNER'),
    ('intermediate', 'INTERMEDIATE'),
    ('advance', 'ADVANCED'),
)


def generate_nine_digit_random_number():
    return get_random_string(length=9, allowed_chars='0123456789ABCDEFGHIJKLMONPQRSTUVWXYZ')


# Create your queryset here.
class CoursesQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

    def featured(self):
        return self.filter(featured=True)

    def category(self, category_slug):
        return Courses.objects.filter(category__category__iexact=category_slug)

    def search(self, query):
        lookup = (Q(title__icontains=query) | Q(title__iexact=query))
        return self.filter(lookup).distinct()

    def get_all(self):
        return self.all()


# Create your manager here.
class CoursesManager(models.Manager):
    def get_queryset(self):
        return CoursesQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().get_all()

    def is_featured(self):
        return self.get_queryset().featured()

    def category(self, category_slug):
        return self.get_queryset().category(category_slug)

    def search(self, query):
        return self.get_queryset().search(query)


# Course models
class Courses(models.Model):
    instructor_id = models.ForeignKey(User, on_delete=models.CASCADE)
    course_id = models.CharField(unique=True, blank=True, max_length=10)
    title = models.CharField('Course Title', max_length=200, null=True, blank=True)
    price = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    course_short_description = models.TextField('Course details', max_length=200, null=True, blank=True)
    course_long_description = RichTextUploadingField()
    will_learn = RichTextField()
    course_image = models.FileField(upload_to=upload_image_path, default='assets/default_images/no-image.png')
    course_intro_video = models.FileField(upload_to=upload_image_path, max_length=500, null=True, blank=True)
    course_intro_video_duration = models.CharField(max_length=20, null=20, blank=True)
    course_complete_duration = models.CharField('Duration', max_length=10)
    course_for = models.CharField(choices=CourseFor, max_length=20, default='Select For')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    file = models.FileField(upload_to=upload_image_path, null=True, blank=True)
    active = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    locked = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=timezone.now)
    update_time = models.DateTimeField(auto_now=timezone.now)
    slug = models.SlugField(blank=True, unique=True)

    objects = CoursesManager()

    # class Meta:
    #     ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('course-detail', kwargs={"slug": self.slug})

    def get_absolute_authenticated_user_url(self):
        return reverse('authenticated-courses-detail', kwargs={"slug": self.slug})

    def get_absolute_update_url(self):
        return reverse("update-courses", kwargs={"slug": self.slug})

    def get_absolute_delete_url(self):
        return reverse("delete-courses", kwargs={"slug": self.slug})


def courses_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


def courses_pre_unique_key_save_receiver(sender, instance, *args, **kwargs):
    if not instance.course_id:
        instance.course_id = generate_nine_digit_random_number()


pre_save.connect(courses_pre_save_receiver, sender=Courses)
pre_save.connect(courses_pre_unique_key_save_receiver, sender=Courses)
