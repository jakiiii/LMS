from django.utils import timezone
from django.db import models

from django.urls import reverse
from django.db.models.signals import pre_save

from instructor.models.professor import Instructor

from lms.utils import unique_slug_generator


class CompanySettingsQuerySet(models.QuerySet):
    pass


class CompanySettingsManager(models.Manager):
    pass


class CompanySettings(models.Model):
    company_name = models.CharField(max_length=250)
    company_address = models.TextField()
    company_email = models.CharField(max_length=32)
    vat_registration_number = models.PositiveIntegerField()
    vat_percentage = models.IntegerField()
    datetime = models.DateTimeField(auto_now_add=timezone.now)
    update = models.DateTimeField(auto_now=timezone.now)

    def __str__(self):
        return self.company_name

    def get_absolute_company_update_url(self):
        return reverse("company-settings-update", kwargs={"slug": self.slug})

    def get_absolute_company_delete_url(self):
        return reverse("company-settings-delete", kwargs={"slug": self.slug})
