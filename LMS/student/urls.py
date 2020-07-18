from django.urls import path
from .views import (
    StudentDashboardView,
    # StudentBrowseLessonsListView,

    StudentProfileView,
    StudentInfoUpdateView,
    MyLessonsListView,
    # episode_cart_home,
    invoice_list,
    invoice_details
)


urlpatterns = [
    path('', StudentDashboardView.as_view(), name='student-dashboard'),
    # path('lessons/', episode_cart_home, name='student-lessons'),
    path('lessons/', MyLessonsListView.as_view(), name='student-lessons'),
    path('profile/', StudentProfileView.as_view(), name='student-profile'),
    path('profile/edit/', StudentInfoUpdateView.as_view(), name='student-profile-edit'),
    path('student_invoice/', invoice_list, name='student_invoice'),
    path('student_invoicedetails/<key>', invoice_details, name='student_invoice_details'),
    # path('browse/lesson/', StudentBrowseLessonsListView.as_view(), name='student-browse-lesson'),
]
