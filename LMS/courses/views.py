from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.core.paginator import Paginator
from django.views.generic import TemplateView, ListView, DetailView

from .models import Courses, Lessons, Episode
from home.models import Header, Testimonial
from category.models import Category
from carts.models import Cart, Invoice

from analytics.mixins import ObjectViewedMixin


# Create your views here.
class CoursesListView(ListView):
    paginate_by = 4
    model = Courses
    template_name = 'courses/courses.html'
    context_object_name = 'courses_context'

    def subscription(self):
        pass

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['category_list'] = Category.objects.all()
        context['category_related_list'] = Courses.objects.all()
        context['header_context'] = Header.objects.all()[:1]
        return context


class CourseDetailsView(ObjectViewedMixin, DetailView):
    model = Courses
    template_name = 'courses/course_details.html'

    def get_context_data(self, *args, **kwargs):
        context = super(CourseDetailsView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj

        context['title'] = '{}'.format(self.get_object().title)
        context['series_context'] = Lessons.objects.filter(course_of__slug=self.get_object().slug)
        context['episode_context'] = Episode.objects.all().filter(lesson_of__slug=self.get_object().slug)
        context['course_total_price'] = Episode.objects.all().filter(lesson_of__slug=self.get_object().slug).aggregate(Sum('price'))['price__sum']
        context['visitor_feedback'] = Testimonial.objects.all()
        context['related_instructor_post'] = Courses.objects.filter(instructor_id=self.object.instructor_id).exclude(id=self.object.id)[:4]
        context['featured_post'] = Courses.objects.all().exclude(id=self.object.id).featured()[:4]
        context['header_context'] = Header.objects.all()[:1]
        if self.request.user.is_authenticated:
            context['invoice_context'] = Invoice.objects.all().filter(student_id=self.request.user)
        return context


class CourseIntroView(ObjectViewedMixin, DetailView):
    model = Courses
    template_name = 'courses/course_intro.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = '{}'.format(self.get_object().title)
        context['header_context'] = Header.objects.all()[:1]
        return context


'''
---------------------------Authenticated User Course View ----------------------------
'''


class AuthenticatedUserCourseDetailsView(LoginRequiredMixin, ObjectViewedMixin, DetailView):
    model = Courses
    template_name = 'courses/authenticated_course_details_view.html'

    def get_context_data(self, *args, **kwargs):
        context = super(AuthenticatedUserCourseDetailsView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        context['title'] = '{}'.format(self.get_object().title)
        context['series_context'] = Lessons.objects.filter(course_of__slug=self.get_object().slug)
        context['episode_context'] = Episode.objects.all().filter(lesson_of__slug=self.get_object().slug)
        episode_context = self.get_episode_context()
        context['episode_context'] = episode_context
        context['page_obj'] = episode_context
        context['student_header'] = 'authenticated-courses-detail'
        context['student_navbar'] = 'authenticated-courses-detail'
        return context

    def get_episode_context(self):
        queryset = Episode.objects.all().filter(lesson_of__slug=self.get_object().slug)
        paginator = Paginator(queryset, 10)
        page = self.request.GET.get('page')
        episode_context = paginator.get_page(page)
        return episode_context
