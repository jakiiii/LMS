from django.contrib import admin
from .models import Courses, Lessons, Episode


# Register your models here.
class EpisodeAdmin(admin.ModelAdmin):
    list_display = ['title', 'series_of', 'lesson_of']


admin.site.register(Courses)
admin.site.register(Lessons)
admin.site.register(Episode, EpisodeAdmin)
