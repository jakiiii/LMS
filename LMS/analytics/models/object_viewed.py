from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from instructor.models import Instructor

from analytics.utils import get_client_ip
from analytics.signals import object_viewed_signals

User = settings.AUTH_USER_MODEL


class ObjectViewed(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    ip_address = models.CharField(max_length=32, null=True, blank=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)       # User, Lesson, Order, Cart, Address
    object_id = models.PositiveSmallIntegerField()      # User id, Lesson id, Series id, Episode id, Order id
    content_object = GenericForeignKey('content_type', 'object_id')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} viewed on {}".format(self.content_type, self.timestamp)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Object viewed'
        verbose_name_plural = 'Objects viewed'


def object_view_receiver(sender, instance, request, *args, **kwargs):
    c_type = ContentType.objects.get_for_model(sender)
    user = None
    if request.user.is_authenticated:
        user = request.user
    new_view_object = ObjectViewed.objects.create(
        user=user,
        content_type=c_type,
        object_id=instance.id,
        ip_address=get_client_ip(request)
    )


object_viewed_signals.connect(object_view_receiver)
