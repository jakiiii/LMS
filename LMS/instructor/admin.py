from django.contrib import admin
from .models import Instructor, Language, Education, Awards, Experience, Certification, CompanySettings


# Register your models here.
admin.site.register(Instructor)
admin.site.register(Education)
admin.site.register(Experience)
admin.site.register(Certification)
admin.site.register(Language)
admin.site.register(Awards)
admin.site.register(CompanySettings)
