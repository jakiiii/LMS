from django.db import models


class LanguageManager(models.Manager):
    pass


class Language(models.Model):
    name = models.CharField(max_length=32)

    objects = LanguageManager()

    def __str__(self):
        return self.name
