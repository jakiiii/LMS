import decimal
from django.contrib.auth.decorators import login_required
from django.db.models import Max
from django.shortcuts import render, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, DetailView, UpdateView
from instructor.models.company_settings import CompanySettings
from accounts.forms import UserInfoChangeForm
from carts.models import Invoice
from courses.models import Courses, Lessons, Episode
from category.models import Category
from accounts.models.email_activation import User
from carts.models import Cart
from orders.models import Order




# Create your views here.
# class StudentDashboardView(TemplateView, LoginRequiredMixin):
#     template_name = 'student/student_dashboard.html'
#
#     def get_context_data(self, *args, **kwargs):
#         context = super(StudentDashboardView, self).get_context_data(*args, **kwargs)
#         context['student_header'] = 'student-dashboard'
#         return context


class StudentDashboardView(LoginRequiredMixin, ListView):
    paginate_by = 4
    model = Courses
    context_object_name = 'courses_context'
    template_name = 'student/student_browse_lesson_view.html'

    def get_context_data(self, *args, **kwargs):
        context = super(StudentDashboardView, self).get_context_data(*args, **kwargs)
        context['category_list'] = Category.objects.all()
        context['student_header'] = 'student-dashboard'
        context['title'] = 'Student Dashboard'
        context['student_navbar'] = 'student-dashboard'
        return context

    def get_login_url(self):
        return reverse('login')


#####################################################################################
# Update Student Information
#####################################################################################


class StudentProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'accounts/user_profile_view.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, *args, **kwargs):
        context = super(StudentProfileView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Update Info'
        context['student_header'] = 'student-profile'
        context['student_navbar'] = 'student-profile'
        return context


class StudentInfoUpdateView(LoginRequiredMixin, UpdateView):
    form_class = UserInfoChangeForm
    template_name = 'accounts/edit_account_profile.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, *args, **kwargs):
        context = super(StudentInfoUpdateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Update Info'
        context['student_header'] = 'student-update-info'
        context['student_navbar'] = 'student-update-info'
        return context

    def get_success_url(self):
        return reverse('student-dashboard')


'''
------------------------ START MY LESSON SECTION --------------------------
'''


class MyLessonsListView(LoginRequiredMixin, ListView):
    model = Invoice
    context_object_name = 'invoice_lesson_context'
    template_name = 'student/my_lesson_view.html'

    def get_context_data(self, *args, **kwargs):
        context = super(MyLessonsListView, self).get_context_data(*args, **kwargs)
        context['title'] = 'My Lessons'
        context['student_header'] = 'student-lessons'
        context['student_navbar'] = 'student-lessons'
        return context

    def get_queryset(self):
        return Invoice.objects.filter(student_id=self.request.user)

# @login_required
# def episode_cart_home(request):
#     cart_obj, new_obj = Cart.objects.new_or_get(request)
#     template_name = 'student/my_lesson_view.html'
#     context = {
#         "cart": cart_obj,
#         "title": 'Cart',
#         "student_header": 'student-lessons',
#         "student_navbar": 'student-lessons'
#     }
#     return render(request, template_name, context)


@login_required
def invoice_list(request):
    invoices = list(Invoice.objects.filter(student_id=request.user).values().distinct('invoice_number'))
    print(invoices)
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    template_name = 'student/invoice_list.html'
    context = {
        "student_header": 'student-lessons',
        "student_navbar": 'student-lessons',
        "invoice": invoices
    }
    return render(request, template_name, context)


@login_required
def invoice_details(request, key):
    company_details = list(CompanySettings.objects.all().values())[0]
    invoice_data = list(
        Invoice.objects.filter(invoice_number=key).values('episode_id__title', 'subtotal', 'invoice_number',
                                                        'issue_date', 'total', 'grand_total', 'vat'))
    return render(request, 'student/invoice_details.html', {
        "company_details": company_details,
        "invoice_data": invoice_data
    })

