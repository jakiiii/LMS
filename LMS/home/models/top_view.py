from django.db import models
from courses.models import Courses


# Top views manager
class TopViewManager(models.Manager):
    pass


# Top views model
class TopView(models.Model):
    course_id = models.ForeignKey(Courses, on_delete=models.CASCADE)
    visitor = models.IntegerField(default=0, blank=True, null=True)
    modified = models.DateField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.course_id
