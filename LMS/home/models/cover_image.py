from django.db import models

from lms.utils_file import upload_image_path


# cover manager
class CoverImageManager(models.Manager):
    pass


# cover model
class CoverImage(models.Model):
    title = models.CharField(max_length=50, null=True, blank=True)
    image = models.ImageField(upload_to=upload_image_path, default='assets/default_images/no-image.png')
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = CoverImageManager()

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return self.title
