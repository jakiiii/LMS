from django.db import models

from ckeditor.fields import RichTextField

from instructor.models.professor import Instructor


class Awards(models.Model):
    professor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    title = models.CharField(max_length=250, null=True, blank=True)
    award_description = models.TextField(max_length=500, null=True, blank=True)
    ex_period = models.DateField(auto_now_add=False, null=True, blank=True)
    ex_end_period = models.DateField(auto_now_add=False, null=True, blank=True)

    def __str__(self):
        return self.title
