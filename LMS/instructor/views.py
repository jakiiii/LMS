import decimal

from django.shortcuts import reverse
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect
from carts.models import Invoice, Cart
from instructor.models.company_settings import CompanySettings
from django.db.models import Count, Sum
from operator import itemgetter

from .forms import (
    CreateBlogPostFrom, CreateCourseForm, InstructorCreationForm, EducationCreationForm, CertificationCreationForm,
    ExperienceCreationForm, LessonsCreationForm, EpisodeCreationForm, CompanySettingsCreationForm
)

from category.models import Category
from .models import Instructor, Education, Certification, Experience, CompanySettings
from blog.models import Blog
from courses.models import Courses, Lessons, Episode
from accounts.models import User


# Create your views here.
class InstructorProfileView(LoginRequiredMixin, ListView):
    model = Courses
    paginate_by = 4
    context_object_name = 'course_list_by_user'
    template_name = 'instructor/admin-dashboard.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = 'Admin Dashboard'
        context['instructor_navbar'] = 'instructor-dashboard'
        return context

    def get_queryset(self):
        return Courses.objects.filter(instructor_id=self.request.user)

    def get_login_url(self):
        return reverse('admin-login')


'''----------------START BLOG GENERIC VIEW -----------------------'''


class InstructorManageBlog(LoginRequiredMixin, ListView):
    model = Blog
    paginate_by = 4
    login_url = '/account/login/'
    context_object_name = 'blog_list_by_user'
    template_name = 'instructor/manage_blog.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = 'Manage Blog'
        context['instructor_navbar'] = 'instructor-blog'
        return context

    def get_queryset(self):
        return Blog.objects.filter(user=self.request.user)


class InstructorBlogPostCreateView(LoginRequiredMixin, CreateView):
    form_class = CreateBlogPostFrom
    login_url = '/account/login/'
    success_url = '/instructor/instructor_blog/'
    template_name = 'instructor/create_blog_post.html'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Blog'
        context['instructor_navbar'] = 'create-blog-post'
        return context


class InstructorBlogUpdateView(LoginRequiredMixin, UpdateView):
    form_class = CreateBlogPostFrom
    template_name = 'instructor/create_blog_post.html'

    def get_queryset(self):
        return Blog.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Post'
        context['instructor_navbar'] = 'update-blog-post'
        return context

    def get_success_url(self):
        return reverse('instructor-blog')

    def get_login_url(self):
        return reverse('login')


class InstructorBlogDeleteView(LoginRequiredMixin, TemplateView):
    pass


'''
----------------END BLOG GENERIC VIEW -------------------------------------
----------------START LESSON / COURSES GENERIC VIEW -----------------------
'''


class InstructorManageCourse(ListView, LoginRequiredMixin):
    model = Courses
    paginate_by = 10
    login_url = '/account/login/'
    context_object_name = 'course_list_by_user'
    template_name = 'instructor/manage-course.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = 'Manage Lesson'
        context['instructor_navbar'] = 'instructor-courses'
        return context

    def get_queryset(self):
        return Courses.objects.filter(instructor_id=self.request.user)


class InstructorCourseCreateView(LoginRequiredMixin, CreateView):
    form_class = CreateCourseForm
    login_url = '/account/login/'
    success_url = '/instructor/instructor_courses/'
    template_name = 'instructor/add-course.html'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.instructor_id = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Lesson'
        context['instructor_navbar'] = 'create-courses'
        return context


class InstructorCourseUpdateView(LoginRequiredMixin, UpdateView):
    form_class = CreateCourseForm
    template_name = 'instructor/add-course.html'

    def get_queryset(self):
        return Courses.objects.filter(instructor_id=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Course'
        context['instructor_navbar'] = 'update-courses'
        return context

    def get_success_url(self):
        return reverse('instructor-courses')

    def get_login_url(self):
        return reverse('login')


class InstructorCourseDeleteView(LoginRequiredMixin, DeleteView):
    model = Courses
    template_name = 'instructor/delete.html'

    def get_context_data(self, **kwargs):
        context = super(InstructorCourseDeleteView, self).get_context_data(**kwargs)
        context['title'] = 'Delete - {}'.format(self.get_object().title)
        context['instructor_navbar'] = 'delete-courses'
        return context

    def get_success_url(self):
        return reverse('instructor-courses')

    def get_login_url(self):
        return reverse('login')


'''
----------------END LESSON / COURSES GENERIC VIEW -------------------------
----------------START SERIES GENERIC VIEW ---------------------------------
'''


class ManageLessonListView(LoginRequiredMixin, ListView):
    paginate_by = 10
    model = Lessons
    login_url = '/account/login/'
    context_object_name = 'series_context'
    template_name = 'instructor/manage-lesson-view.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = 'Lessons'
        context['instructor_navbar'] = 'manage-lesson'
        context['related_course'] = Courses.objects.all()
        return context


class ManageLessonCreateView(LoginRequiredMixin, CreateView):
    form_class = LessonsCreationForm
    login_url = '/account/login/'
    success_url = '/instructor/manage/lesson/'
    template_name = 'instructor/create-lesson-view.html'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.instructor_id = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add Lesson'
        context['instructor_navbar'] = 'create-lesson'
        return context


class SeriesUpdateView(LoginRequiredMixin, UpdateView):
    form_class = LessonsCreationForm
    template_name = 'instructor/create-lesson-view.html'

    def get_queryset(self):
        return Lessons.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Series'
        context['instructor_navbar'] = 'update-series'
        return context

    def get_login_url(self):
        return reverse('login')

    def get_success_url(self):
        return reverse('manage-lesson')


class SeriesDeleteView(LoginRequiredMixin, DeleteView):
    model = Lessons
    template_name = 'instructor/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete - {}'.format(self.get_object().title)
        context['instructor_navbar'] = 'delete-lesson'
        return context

    def get_success_url(self):
        return reverse('manage-lesson')

    def get_login_url(self):
        return reverse('login')


'''
----------------END SERIES GENERIC VIEW ------------------------------------
----------------START EPISODE GENERIC VIEW ---------------------------------
'''


class ManageEpisodeView(LoginRequiredMixin, ListView):
    paginate_by = 10
    model = Episode
    login_url = '/account/login/'
    context_object_name = 'episode_context'
    template_name = 'instructor/manage-episode-view.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = 'Episode'
        context['instructor_navbar'] = 'manage-episode'
        context['related_series'] = Lessons.objects.all()
        context['related_course'] = Courses.objects.all()
        return context


class EpisodeCreateView(LoginRequiredMixin, CreateView):
    form_class = EpisodeCreationForm
    template_name = 'instructor/create-episode-view.html'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.instructor_id = self.request.user
        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = 'Add Episode'
        context['instructor_navbar'] = 'create-episode'
        return context

    def get_login_url(self):
        return reverse('login')

    def get_success_url(self):
        return reverse('manage-episode')


class UpdateEpisodeView(LoginRequiredMixin, UpdateView):
    form_class = EpisodeCreationForm
    template_name = 'instructor/create-episode-view.html'

    def get_queryset(self):
        return Episode.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Episode'
        context['instructor_navbar'] = 'update-episode'
        return context

    def get_login_url(self):
        return reverse('login')

    def get_success_url(self):
        return reverse('manage-episode')


class DeleteEpisodeView(LoginRequiredMixin, DeleteView):
    model = Episode
    template_name = 'instructor/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete - {}'.format(self.get_object().title)
        context['instructor_navbar'] = 'delete-episode'
        return context

    def get_success_url(self):
        return reverse('manage-episode')

    def get_login_url(self):
        return reverse('login')


'''
----------------END EPISODE GENERIC VIEW --------------------------------------------------
----------------START PROFESSOR / INSTRUCTOR GENERIC VIEW ---------------------------------
'''


class InstructorManageView(LoginRequiredMixin, ListView):
    paginate_by = 10
    model = Instructor
    context_object_name = 'instructor_context'
    template_name = 'instructor/instructor_manage_view.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = 'Manage Professor'
        context['instructor_navbar'] = 'instructor-manage'
        return context

    def get_login_url(self):
        return reverse('login')


class NewInstructorCreateView(LoginRequiredMixin, CreateView):
    form_class = InstructorCreationForm
    login_url = '/account/login/'
    success_url = '/instructor/manage/'
    template_name = 'instructor/instructor_add_view.html'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add Instructor'
        context['instructor_navbar'] = 'instructor-create'
        return context


class InstructorUpdateView(LoginRequiredMixin, UpdateView):
    form_class = InstructorCreationForm
    template_name = 'instructor/instructor_add_view.html'

    def get_queryset(self):
        return Instructor.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Professor'
        context['instructor_navbar'] = 'instructor-update'
        return context

    def get_success_url(self):
        return reverse('instructor-manage')

    def get_login_url(self):
        return reverse('login')


class InstructorDeleteView(LoginRequiredMixin, DeleteView):
    model = Instructor
    template_name = 'instructor/delete.html'

    def get_context_data(self, **kwargs):
        context = super(InstructorDeleteView, self).get_context_data(**kwargs)
        context['title'] = 'Delete - {}'.format(self.get_object().title)
        context['instructor_navbar'] = 'delete-courses'
        return context

    def get_success_url(self):
        return reverse('instructor-manage')

    def get_login_url(self):
        return reverse('login')


class EducationManageView(LoginRequiredMixin, ListView):
    paginate_by = 10
    model = Education
    context_object_name = 'education_context'
    template_name = 'instructor/education-manage-view.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = 'Professor Education'
        context['instructor_navbar'] = 'education-manage'
        return context

    def get_login_url(self):
        return reverse('login')


class CertificationManageView(LoginRequiredMixin, ListView):
    paginate_by = 10
    model = Certification
    context_object_name = 'certification_context'
    template_name = 'instructor/certification-manage-view.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = 'Professor Certification'
        context['instructor_navbar'] = 'certification-manage'
        return context

    def get_login_url(self):
        return reverse('login')


class ExperienceManageView(LoginRequiredMixin, ListView):
    paginate_by = 10
    model = Experience
    context_object_name = 'experience_context'
    template_name = 'instructor/experience-manage-view.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = 'Professor Experience'
        context['instructor_navbar'] = 'experience-manage'
        return context

    def get_login_url(self):
        return reverse('login')


class EducationCreateView(LoginRequiredMixin, CreateView):
    form_class = EducationCreationForm
    template_name = 'instructor/education-create-view.html'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add Certificate'
        context['instructor_navbar'] = 'education-create'
        return context

    def get_login_url(self):
        return reverse('login')

    def get_success_url(self):
        return reverse('education-manage')


class CertificationCreateView(LoginRequiredMixin, CreateView):
    form_class = CertificationCreationForm
    template_name = 'instructor/certification-create-view.html'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add Certification'
        context['instructor_navbar'] = 'certification-manage'
        return context

    def get_login_url(self):
        return reverse('login')

    def get_success_url(self):
        return reverse('certification-manage')


class ExperienceCreateView(LoginRequiredMixin, CreateView):
    form_class = ExperienceCreationForm
    template_name = 'instructor/experience-create-view.html'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add Experience'
        context['instructor_navbar'] = 'experience-manage'
        return context

    def get_login_url(self):
        return reverse('login')

    def get_success_url(self):
        return reverse('experience-manage')


class EducationUpdateView(LoginRequiredMixin, UpdateView):
    form_class = EducationCreationForm
    template_name = 'instructor/education-create-view.html'

    def get_queryset(self):
        return Education.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Certificate'
        context['instructor_navbar'] = 'certification-update'
        return context

    def get_login_url(self):
        return reverse('login')

    def get_success_url(self):
        return reverse('education-manage')


class CertificationUpdateView(LoginRequiredMixin, UpdateView):
    form_class = CertificationCreationForm
    template_name = 'instructor/certification-create-view.html'

    def get_queryset(self):
        return Certification.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Certification'
        context['instructor_navbar'] = 'certification-update'
        return context

    def get_login_url(self):
        return reverse('login')

    def get_success_url(self):
        return reverse('certification-manage')


class ExperienceUpdateView(LoginRequiredMixin, UpdateView):
    form_class = ExperienceCreationForm
    template_name = 'instructor/experience-create-view.html'

    def get_queryset(self):
        return Experience.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Experience'
        context['instructor_navbar'] = 'experience-update'
        return context

    def get_login_url(self):
        return reverse('login')

    def get_success_url(self):
        return reverse('experience-manage')


class EducationDeleteView(LoginRequiredMixin, DeleteView):
    model = Education
    template_name = 'instructor/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete - {}'.format(self.get_object().title)
        context['instructor_navbar'] = 'education-delete'
        return context

    def get_login_url(self):
        return reverse('login')

    def get_success_url(self):
        return reverse('education-manage')


class CertificationDeleteView(LoginRequiredMixin, DeleteView):
    model = Certification
    template_name = 'instructor/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete - {}'.format(self.get_object().title)
        context['instructor_navbar'] = 'certification-delete'
        return context

    def get_login_url(self):
        return reverse('login')

    def get_success_url(self):
        return reverse('certification-manage')


class ExperienceDeleteView(LoginRequiredMixin, DeleteView):
    model = Experience
    template_name = 'instructor/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete - {}'.format(self.get_object().title)
        context['instructor_navbar'] = 'experience-delete'
        return context

    def get_login_url(self):
        return reverse('login')

    def get_success_url(self):
        return reverse('experience-manage')


'''
----------------END PROFESSOR / INSTRUCTOR GENERIC VIEW ------------------------------
----------------START COMPANY SETTINGS GENERIC VIEW ----------------------------------
'''


class CompanySettingListView(LoginRequiredMixin, ListView):
    model = CompanySettings
    paginate_by = 10
    context_object_name = 'company_context'
    template_name = 'instructor/manage-company-seetings-view.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = 'Company Settings'
        context['instructor_navbar'] = 'company-settings'
        return context

    def get_login_url(self):
        return reverse('login')


class CompanySettingCreateView(LoginRequiredMixin, CreateView):
    form_class = CompanySettingsCreationForm
    template_name = 'instructor/create-company-seetings-view.html'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add Company Info'
        context['instructor_navbar'] = 'company-settings-create'
        return context

    def get_login_url(self):
        return reverse('login')

    def get_success_url(self):
        return reverse('company-settings')


class CompanySettingUpdateView(LoginRequiredMixin, TemplateView):
    form_class = CompanySettingsCreationForm
    template_name = 'instructor/create-company-seetings-view.html'

    def get_queryset(self):
        return Experience.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Company Info'
        context['instructor_navbar'] = 'company-settings-update'
        return context

    def get_login_url(self):
        return reverse('login')

    def get_success_url(self):
        return reverse('company-settings')


class CompanySettingDeleteView(LoginRequiredMixin, TemplateView):
    pass


'''
----------------END PROFESSOR / INSTRUCTOR GENERIC VIEW ------------------------------
----------------START STUDENT GENERIC VIEW -------------------------------------------
'''


class StudentAdminListView(LoginRequiredMixin, ListView):
    paginate_by = 10
    model = User
    context_object_name = 'student_mange_info'
    template_name = 'instructor/student_list_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Student Information'
        context['instructor_navbar'] = 'manage-student-admin'
        return context

    def get_queryset(self):
        return User.objects.all().is_student()


class StudentAdminUpdateView(LoginRequiredMixin, TemplateView):
    pass


class StudentAdminDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'instructor/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete - {}'.format(self.get_object().title)
        context['instructor_navbar'] = 'delete-user'
        return context

    def get_success_url(self):
        return reverse('manage-student-admin')

    def get_login_url(self):
        return reverse('login')


'''
----------------END START MESSAGE GENERIC VIEW ------------------------------
----------------START REPORT VIEW -------------------------------------------
'''


def category_professor(request):
    courses = list(Episode.objects.values(
        'episode_instructor__id',
        'lesson_of__category__category',
        'lesson_of__subcategory__id',
        'lesson_of__subcategory__subcategory',
        'episode_instructor__first_name',
        'episode_instructor__last_name',
        'episode_instructor__phone',
        'episode_instructor__image',
        'episode_instructor__email',

    ).order_by('episode_instructor__id').annotate(total_episode=Count('lesson_of__subcategory__id')))
    template_name = 'instructor/category_professor.html'
    context = {
        "instructor_navbar": 'manage-student-admin',
        "courses": courses
    }
    return render(request, template_name, context)


def top_sales_videos_professor(request):
    data = Invoice.objects.values(
        'episode_id__episode_instructor__id',
        'episode_id__lesson_of__category__category',
        'episode_id__lesson_of__subcategory__subcategory',
        'episode_id__episode_instructor__first_name',
        'episode_id__episode_instructor__last_name',
        'episode_id__episode_instructor__phone',
        'episode_id__episode_instructor__image',
        'episode_id__episode_instructor__email',
        'episode_id__episode_instructor__user'
    ).annotate(the_count=Count('episode_id__episode_instructor__id')).order_by('-the_count')

    template_name = 'instructor/top_sales_videos_professor.html'
    context = {
        "instructor_navbar": 'manage-student-admin',
        "data": data
    }
    return render(request, template_name, context)


def top_paid_videos_professor(request):
    data = Invoice.objects.values(
        'episode_id__episode_instructor__id',
        'episode_id__lesson_of__category__category',
        'episode_id__lesson_of__subcategory__subcategory',
        'episode_id__episode_instructor__first_name',
        'episode_id__episode_instructor__last_name',
        'episode_id__episode_instructor__phone',
        'episode_id__episode_instructor__image',
        'episode_id__episode_instructor__email',
        'episode_id__episode_instructor__user',
    ).annotate(the_count=Count('episode_id__episode_instructor__id')).order_by('-the_count')

    for item in data:
        instructor_episodes = Invoice.objects.filter(
            episode_id__episode_instructor__id=item['episode_id__episode_instructor__id']).values_list(
            'episode_id__price')
        total = decimal.Decimal(0)
        for price in instructor_episodes:
            total += price[0]
        item['total'] = total

    data = sorted(list(data), key=itemgetter('total'), reverse=True)
    template_name = 'instructor/top_paid_videos_professor.html'
    context = {
        "instructor_navbar": 'manage-student-admin',
        "data": data
    }
    return render(request, template_name, context)


def top_private_lesson_contact_professor(request):
    template_name = 'instructor/top_private_lesson_contact_professor.html'
    context = {
        "instructor_navbar": 'manage-student-admin',
    }
    return render(request, template_name, context)


def top_viewing_professor(request):
    template_name = 'instructor/top_viewing_professor.html'
    context = {
        "instructor_navbar": 'manage-student-admin',
    }
    return render(request, template_name, context)


def top_self_professor(request):
    template_name = 'instructor/top_self_professor.html'
    context = {
        "instructor_navbar": 'manage-student-admin',
    }
    return render(request, template_name, context)


def fewer_videos_professor(request):
    data = list(Episode.objects.values(
        'episode_instructor__id',
        'lesson_of__category__category',
        'lesson_of__subcategory__subcategory',
        'episode_instructor__first_name',
        'episode_instructor__last_name',
        'episode_instructor__phone',
        'episode_instructor__image',
        'episode_instructor__email',
        'episode_instructor__user',

    ).annotate(the_count=Count('episode_instructor__id')).order_by('-the_count'))
    print(data)
    count = 0
    while count < len(data):
        if data[count]['the_count'] > 5:
            data.pop(count)
            count = count - 1
        count += 1

    template_name = 'instructor/fewer_videos_professor.html'
    context = {
        "instructor_navbar": 'manage-student-admin',
        "data": data
    }
    return render(request, template_name, context)


# def top_self_professor(request):
#     template_name = 'instructor/top_self_professor.html'
#     context = {
#         "instructor_navbar": 'manage-student-admin',
#     }
#     return render(request, template_name, context)


def sales(request):
    template_name = 'instructor/sales.html'
    context = {
        "instructor_navbar": 'manage-student-admin',
    }
    return render(request, template_name, context)


def series_wise_sales_report(request):
    data = list(Invoice.objects.values(
        'episode_id__series_of__id',
        'episode_id__series_of__lesson_title',
    ).order_by('episode_id__series_of__id').annotate(price_sum=Sum('subtotal'), total_episode=Count('episode_id_id')))
    vat_percentage = CompanySettings.objects.all().values_list('vat_percentage',  flat=True)[0]
    count = 0
    for item in data:
        data[count]['vat'] = vat_percentage
        data[count]['total_price_adding_vat'] = item['price_sum'] + (decimal.Decimal(vat_percentage)/100) * item['price_sum']
        count += 1
    template_name = 'instructor/series_wise_sales_report.html'
    context = {
        "instructor_navbar": 'manage-student-admin',
        "data": data
    }
    return render(request, template_name, context)


def professor_wise_sales_report(request):
    data = list(Invoice.objects.values(
        'episode_id__episode_instructor__id',
        'episode_id__episode_instructor__first_name',
        'episode_id__episode_instructor__last_name',
    ).order_by('episode_id__episode_instructor__id').annotate(price_sum=Sum('subtotal'), total_episode=Count('episode_id_id')))
    vat_percentage = CompanySettings.objects.all().values_list('vat_percentage', flat=True)[0]
    count = 0
    for item in data:
        data[count]['vat'] = vat_percentage
        data[count]['total_price_adding_vat'] = item['price_sum'] + (decimal.Decimal(vat_percentage) / 100) * item[
            'price_sum']
        count += 1
    print(data)
    template_name = 'instructor/professor_wise_sales_report.html'
    context = {
        "instructor_navbar": 'manage-student-admin',
        "data": data
    }
    return render(request, template_name, context)


def settings(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        address = request.POST['address']
        vat_registration_number = request.POST['vat_registration_number']
        vat_percentage = request.POST['vat_percentage']
        try:
            CompanySettings.objects.all().delete()
            CompanySettings.objects.create(
                company_name=name,
                company_address=address,
                company_email=email,
                vat_registration_number=vat_registration_number,
                vat_percentage=vat_percentage
            )
        except:
            pass
    data = list(CompanySettings.objects.all().values())[0]
    template_name = 'instructor/company_settings.html'
    context = {
        "instructor_navbar": 'manage-student-admin',
        "data": data
    }
    return render(request, template_name, context)


def invoice_list(request):
    invoices = list(Invoice.objects.filter().values().distinct('invoice_number'))
    template_name = 'instructor/invoice_list_copy.html'
    context = {
        "instructor_navbar": 'manage-student-admin',
        "invoice": invoices
    }
    return render(request, template_name, context)


def invoice_details(request, key):
    company_details = list(CompanySettings.objects.all().values())[0]
    invoice_data = list(
        Invoice.objects.filter(invoice_number=key).values('episode_id__title', 'subtotal', 'invoice_number', 'vat',
                                                          'issue_date', 'total', 'grand_total'))
    return render(request, 'instructor/invoice_details.html', {
        "company_details": company_details,
        "invoice_data": invoice_data
    })
