from django.shortcuts import render, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView

from courses.models import Courses, Lessons, Episode
from instructor.models import Instructor
from blog.models import Blog
from accounts.models import User
from carts.models import Invoice
from home.models import Header


# Create your views here.
class AdministratorLessonSearchView(LoginRequiredMixin, ListView):
    paginate_by = 10
    model = Courses
    context_object_name = 'course_list_by_user'
    template_name = 'instructor/manage-course.html'

    def get_context_data(self, *args, **kwargs):
        context = super(AdministratorLessonSearchView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Manage Lesson'
        context['instructor_navbar'] = 'lesson-search-query'
        return context

    def get_login_url(self):
        return reverse('login')

    def get_queryset(self):
        request = self.request
        query = request.GET.get('q', None)
        if query is not None:
            return Courses.objects.search(query)
        return Courses.objects.none()


class AdministratorSeriesSearchView(LoginRequiredMixin, ListView):
    paginate_by = 5
    model = Lessons
    context_object_name = 'series_context'
    template_name = 'instructor/manage-lesson-view.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = 'Lessons'
        context['instructor_navbar'] = 'lesson-series-query'
        context['related_course'] = Courses.objects.all()
        return context

    def get_login_url(self):
        return reverse('login')

    def get_queryset(self):
        request = self.request
        query = request.GET.get('q', None)
        if query is not None:
            return Lessons.objects.search(query)
        return Lessons.objects.none()


class AdministratorEpisodeSearchView(LoginRequiredMixin, ListView):
    paginate_by = 10
    model = Episode
    context_object_name = 'episode_context'
    template_name = 'instructor/manage-episode-view.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = 'Episode'
        context['instructor_navbar'] = 'episode-search-query'
        return context

    def get_login_url(self):
        return reverse('login')

    def get_queryset(self):
        request = self.request
        query = request.GET.get('q', None)
        if query is not None:
            data = Episode.objects.search(query)
            print('PRINT', data)
            return data
        return Episode.objects.none()


class AdministratorProfessorSearchView(LoginRequiredMixin, ListView):
    paginate_by = 10
    model = Instructor
    context_object_name = 'instructor_context'
    template_name = 'instructor/instructor_manage_view.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = 'Manage Blog'
        context['instructor_navbar'] = 'instructor-manage'
        return context

    def get_queryset(self):
        request = self.request
        query = request.GET.get('q', None)
        if query is not None:
            return Instructor.objects.search(query)
        return Instructor.objects.none()


class AdministratorStudentSearchView(LoginRequiredMixin, ListView):
    paginate_by = 10
    model = User
    context_object_name = 'student_mange_info'
    template_name = 'instructor/student_list_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Student Information'
        context['instructor_navbar'] = 'student-search-query'
        return context

    def get_queryset(self):
        request = self.request
        query = request.GET.get('q', None)
        if query is not None:
            return User.objects.search(query)
        return User.objects.none()


class StudentMyLessonSearchView(LoginRequiredMixin, ListView):
    model = Invoice
    context_object_name = 'invoice_lesson_context'
    template_name = 'student/my_lesson_view.html'

    def get_context_data(self, *args, **kwargs):
        context = super(StudentMyLessonSearchView, self).get_context_data(*args, **kwargs)
        context['title'] = 'My Lesson'
        context['student_navbar'] = 'mylesson-search-query'
        return context

    def get_queryset(self):
        request = self.request
        query = request.GET.get('q', None)
        if query is not None:
            return Invoice.objects.search(query)
        return Invoice.objects.none()


class ProfessorListSearchView(ListView):
    paginate_by = 8
    model = Instructor
    context_object_name = 'professor_context'
    template_name = 'home/professor_all_view.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['header_context'] = Header.objects.all()[:1]
        context['title'] = 'Professor'
        return context

    def get_queryset(self):
        query = self.request.GET.get('q', None)
        if query is not None:
            return Instructor.objects.search(query)
        return Instructor.objects.none()
