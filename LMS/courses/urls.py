from django.urls import path

from .views import (
    CoursesListView,
    CourseDetailsView,
    CourseIntroView,
    AuthenticatedUserCourseDetailsView
)


urlpatterns = [
    path('courses/', CoursesListView.as_view(), name='courses'),
    path('course_detail/<slug:slug>/', CourseDetailsView.as_view(), name='course-detail'),
    path('course_intro/<slug:slug>/', CourseIntroView.as_view(), name='courses-intro'),
    path('student/course/detail/<slug:slug>/', AuthenticatedUserCourseDetailsView.as_view(), name='authenticated-courses-detail'),
]
