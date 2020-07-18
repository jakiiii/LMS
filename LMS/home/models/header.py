from django.db import models

from lms.utils_file import upload_image_path


# cover manager
class HeaderManager(models.Manager):
    pass


# cover model
class Header(models.Model):
    logo = models.ImageField(upload_to=upload_image_path, default='assets/default_images/no-image.png')
    header_title = models.CharField(max_length=50, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = HeaderManager()

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return self.header_title
