from django.db import models


UrlFor = (
    ('courses_url', 'courses_url'),
    ('register_url', 'register_url'),
)


# cover manager
class CoverManager(models.Manager):
    pass


# cover model
class Cover(models.Model):
    cover_title_not_authenticated = models.CharField(max_length=50, null=True, blank=True)
    cover_text_not_authenticated = models.TextField(max_length=400, null=True, blank=True)
    url_link_not_authenticated = models.CharField(choices=UrlFor, max_length=25, null=True, blank=True)
    url_btn_not_authenticated = models.CharField(max_length=25, null=True, blank=True)
    cover_title_authenticated = models.CharField(max_length=50, null=True, blank=True)
    cover_text_authenticated = models.TextField(max_length=400, null=True, blank=True)
    url_link_authenticated = models.CharField(choices=UrlFor, max_length=25, null=True, blank=True)
    url_btn_authenticated = models.CharField(max_length=25, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = CoverManager()

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return self.cover_title_not_authenticated
