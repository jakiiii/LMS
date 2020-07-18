from django.urls import path
from .views import (
    UserLoginView,
    AdminLoginView,
    UserRegistrationView,
    AccountEmailActivateView,
    UserRegistrationPaymentCreateView,
    BillingView,
    PaymentView,
    BillingPaymentView,
    get_logout,

    UserInfoUpdateView,
    UserProfileView,
)


urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('admin/login/', AdminLoginView.as_view(), name='admin-login'),
    path('signup/', UserRegistrationView.as_view(), name='register'),
    path('email/confirmed/<key>/', AccountEmailActivateView.as_view(), name='email-activate'),
    path('registration/payment/', UserRegistrationPaymentCreateView.as_view(), name='registration-payment'),
    path('billing/', BillingView.as_view(), name='instructor-billing'),
    path('payments/', PaymentView.as_view(), name='instructor-payments'),
    path('billing/payments/', BillingPaymentView.as_view(), name='billing-payments'),
    path('logout/', get_logout, name='logout'),

    path('update/info/', UserInfoUpdateView.as_view(), name='profile-update-info'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
]
