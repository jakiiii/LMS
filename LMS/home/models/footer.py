from django.db import models

from lms.utils_file import upload_image_path


# cover manager
class FooterManager(models.Manager):
    pass


# cover model
class Footer(models.Model):
    logo = models.ImageField(upload_to=upload_image_path, default='assets/default_images/no-image.png')
    footer_title = models.CharField(max_length=50, null=True, blank=True)
    footer_description = models.TextField(max_length=800, null=True, blank=True)
    copyright_quote = models.CharField(max_length=150, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = FooterManager()

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return self.footer_title
