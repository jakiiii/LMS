from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL


class UserSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    ip_address = models.CharField(max_length=220, null=True, blank=True)  # IP Fields
    session_key = models.CharField(max_length=120, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    ended = models.BooleanField(default=False)
