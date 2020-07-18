from django.shortcuts import render, redirect, reverse
from django.views.generic import FormView, CreateView, View, UpdateView, DetailView, TemplateView
from django.views.generic.edit import FormMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.http import is_safe_url
from django.utils.safestring import mark_safe
from django.contrib.messages.views import SuccessMessageMixin, messages

from .forms import UserLoginForm, UserRegistrationForm, ReactivateEmailFrom, UserInfoChangeForm
from .models.email_activation import User, EmailActivation

from lms.mixins import NextUrlMixin, RequestFormAttachMixin
from .signals import user_logged_in
from .mixins import UserViewedMixin


# Create your views here.
class UserLoginView(NextUrlMixin, RequestFormAttachMixin, FormView):
    form_class = UserLoginForm
    success_url = '/student/'
    default_next = '/student/'
    template_name = 'accounts/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('student-dashboard')
        else:
            return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        next_path = self.get_next_url()
        return redirect(next_path)

    def get_context_data(self, **kwargs):
        context = super(UserLoginView, self).get_context_data(**kwargs)
        context['title'] = 'Login'
        return context


class AdminLoginView(NextUrlMixin, RequestFormAttachMixin, FormView):
    form_class = UserLoginForm
    success_url = '/instructor/'
    default_next = '/instructor/'
    template_name = 'accounts/admin-login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('instructor-dashboard')
        else:
            return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        next_path = self.get_next_url()
        return redirect(next_path)

    def get_context_data(self, **kwargs):
        context = super(AdminLoginView, self).get_context_data(**kwargs)
        context['title'] = 'Login'
        return context


class UserRegistrationView(SuccessMessageMixin, CreateView):
    form_class = UserRegistrationForm
    template_name = 'accounts/registration.html'
    success_message = 'Registration successful. We send activation instruction on your email.'
    # success_url = '/account/registration/payment/'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('instructor-dashboard')
        else:
            return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UserRegistrationView, self).get_context_data(**kwargs)
        context['title'] = 'Sign Up'
        return context

    def get_success_url(self):
        return reverse('login')


class AccountEmailActivateView(FormMixin, View):
    success_url = '/account/login/'
    form_class = ReactivateEmailFrom
    key = None

    def get(self, request, key=None, *args, **kwargs):
        if key is not None:
            qs = EmailActivation.objects.filter(key__iexact=key)
            confirm_qs = qs.conformable()
            if confirm_qs.count() == 1:
                obj = confirm_qs.first()
                obj.activate()
                messages.success(self.request, "Your email has been confirmed. You can login now.")
                return redirect('login')
            else:
                activated_qs = qs.filter(key__iexact=key, activated=True)
                if activated_qs.exists():
                    reset_link = reverse('password_reset')
                    msg = """Your email has already confirmed!
                    Did you mean <a href="{link}">reset your password</a>?
                    """.format(link=reset_link)
                    messages.info(self.request, mark_safe(msg))
                    return redirect('login')
        context = {
            'form': self.get_form(),
            'key': self.key
        }
        return render(self.request, 'registration/activation_error.html', context)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        msg = "Your account activation link sent. Please check your email."
        messages.success(self.request, msg)
        email = form.cleaned_data.get("email")
        obj = EmailActivation.objects.email_exists(email).first()
        user = obj.user
        new_activation = EmailActivation.objects.create(user=user, email=email)
        new_activation.send_activation()
        return super(AccountEmailActivateView, self).form_valid(form)

    def form_invalid(self, form):
        context = {
            "form": form,
            "key": self.key
        }
        return render(self.request, 'registration/activation_error.html', context)


class UserRegistrationPaymentCreateView(TemplateView):
    template_name = 'accounts/registration-payment.html'


#####################################################################################
# Update SuperAdmin and Student Information
#####################################################################################

class UserProfileView(DetailView, LoginRequiredMixin):
    model = User
    template_name = 'accounts/user_profile_view.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, *args, **kwargs):
        context = super(UserProfileView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Update Info'
        context['instructor_navbar'] = 'user-profile'
        return context


class UserInfoUpdateView(UpdateView, LoginRequiredMixin):
    form_class = UserInfoChangeForm
    template_name = 'accounts/edit_account_profile.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, *args, **kwargs):
        context = super(UserInfoUpdateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Update Info'
        context['instructor_navbar'] = 'profile-update-info'
        return context

    def get_success_url(self):
        return reverse('instructor-dashboard')


class BillingView(TemplateView, LoginRequiredMixin):
    template_name = 'accounts/billing_view.html'


class PaymentView(TemplateView, LoginRequiredMixin):
    template_name = 'accounts/payments_view.html'


class BillingPaymentView(TemplateView, LoginRequiredMixin):
    template_name = 'accounts/billing_payment_view.html'


def get_logout(request):
    logout(request)
    return redirect('index')
