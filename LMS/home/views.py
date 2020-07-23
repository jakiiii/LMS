from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from django.db.models import Count

from .models import Header, Cover, CoverImage, Footer, TopView, Testimonial
from courses.models import Courses, Lessons, Episode
from category.models import Subcategory
from instructor.models import Instructor, Experience, Certification, Awards
from blog.models import Blog


# Create your views here.
class HomeListView(ListView):
    paginate_by = 4
    model = Courses
    template_name = 'home/home.html'
    context_object_name = 'home_content'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['series_count'] = Lessons.objects.all().count()
        context['episode_count'] = Episode.objects.all().count()
        context['banner_image'] = 'index'
        context['banner_info'] = 'index'
        # context['footer'] = 'index'
        context['header_context'] = Header.objects.all()[:1]
        context['cover_images'] = CoverImage.objects.all()[:10]
        context['cover_info'] = Cover.objects.all()[:10]
        # context['footer_context'] = Footer.objects.all()[:1]
        context['learning_path'] = Subcategory.objects.annotate(course_count=Count('subcategory'))[:9]
        context['blog_context'] = Blog.objects.all()[:3]
        context['visitor_feedback'] = Testimonial.objects.all()
        return context


class ProfessorListView(ListView):
    paginate_by = 8
    model = Instructor
    context_object_name = 'professor_context'
    template_name = 'home/professor_all_view.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['header_context'] = Header.objects.all()[:1]
        context['title'] = 'Professor'
        return context


class ProfessorDetailView(DetailView):
    model = Instructor
    context_object_name = 'instructor_object'
    template_name = 'home/professor_view.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ProfessorDetailView, self).get_context_data(*args, **kwargs)
        context['title'] = '{} {}'.format(self.get_object().first_name, self.get_object().last_name)
        context['experience_context'] = Experience.objects.filter(professor=self.object.id)
        context['certification_context'] = Certification.objects.filter(professor=self.object.id)
        context['instructor_episode'] = Episode.objects.filter(episode_instructor=self.object.id)
        context['featured_lessons'] = Courses.objects.all().featured()[:4]
        context['header_context'] = Header.objects.all()[:1]
        return context
