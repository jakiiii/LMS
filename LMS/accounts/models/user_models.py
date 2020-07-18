from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils import timezone
from django.db.models.signals import pre_save

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager
)

# from accounts.models import Role
from lms.utils_file import upload_image_path
from lms.utils import unique_slug_generator


# Create user QuerySet here
class UserQuerySet(models.QuerySet):
    def is_student(self):
        return self.filter(is_student=True)

    def search(self, query):
        loopup = (
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query)
        )
        return self.filter(loopup).distinct()


# Create your manager here.
class UserManager(BaseUserManager):
    def get_queryset(self):
        return UserQuerySet(self.model, using=self._db)

    def search(self, query):
        # return self.get_queryset().search(query)
        return self.get_queryset().is_student().search(query)

    def is_student(self):
        return self.get_queryset().is_student()

    def create_user(self, email, first_name, last_name, password=None, is_active=True,
                    is_staff=False, is_student=False, is_admin=False):
        if not first_name:
            raise ValueError("Please, type your first name.")
        if not last_name:
            raise ValueError("Please type your last name.")
        if not email:
            raise ValueError('User have to an email address!')
        if not password:
            raise ValueError('User must have a password!')
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)
        user.is_active = is_active
        user.staff = is_staff
        user.is_student = is_student
        user.admin = is_admin
        user.save(using=self._db)
        return user

    def create_staff(self, email, first_name, last_name, password=None):
        user = self.create_user(
            email,
            first_name,
            last_name,
            password=password,
            is_staff=True
        )
        return user

    def create_student(self, email, first_name, last_name, password=None):
        user = self.create_user(
            email,
            first_name,
            last_name,
            password=password,
            is_student=True
        )
        return user

    def create_superuser(self, email, first_name, last_name, password=None):
        user = self.create_user(
            email,
            first_name,
            last_name,
            password=password,
            is_student=True,
            is_staff=True,
            is_admin=True
        )
        return user


# Create your models here.
class User(AbstractBaseUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(verbose_name='Email', max_length=32, unique=True)
    image = models.FileField(upload_to=upload_image_path, default='assets/default_images/no-image.png')
    about = models.TextField(max_length=400, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_management = models.BooleanField(default=False)
    # user_role = models.ForeignKey(Role, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(blank=True, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    objects = UserManager()

    def __str__(self):
        return self.email

    def get_first_name(self):
        return self.first_name

    def get_last_name(self):
        return self.last_name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def student(self):
        return self.is_student

    # @property
    # def is_active(self):
    #     return self.active

    @property
    def title(self):
        return self.last_name

    def get_absolute_url(self):
        return reverse('user', kwargs={"slug": self.slug})

    def get_absolute_user_update_url(self):
        return reverse('profile-update-info', kwargs={"slug": self.slug})

    def get_absolute_user_update_by_admin_url(self):
        return reverse('update-user-admin', kwargs={"slug": self.slug})

    def get_absolute_user_delete_url(self):
        return reverse("delete-user", kwargs={"slug": self.slug})


def user_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(user_pre_save_receiver, sender=User)
