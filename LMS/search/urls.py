from django.urls import path

from .views import (
    AdministratorLessonSearchView,
    AdministratorSeriesSearchView,
    AdministratorEpisodeSearchView,
    AdministratorProfessorSearchView,
    AdministratorStudentSearchView
)


urlpatterns = [
    path('instructor/instructor_courses/search/', AdministratorLessonSearchView.as_view(), name='lesson-search-query'),
    path('instructor/manage/lesson/search/', AdministratorSeriesSearchView.as_view(), name='lesson-series-query'),
    path('instructor/manage/episode/search/', AdministratorEpisodeSearchView.as_view(), name='episode-search-query'),
    path('instructor/manage/search/', AdministratorProfessorSearchView.as_view(), name='professor-series-query'),
    path('instructor/manage/student/search/', AdministratorStudentSearchView.as_view(), name='student-search-query'),
]
