from django.urls import path

from .views import (
    HomeListView,
    ProfessorDetailView,
    ProfessorListView,
)


urlpatterns = [
    path('', HomeListView.as_view(), name='index'),
    path('professor/', ProfessorListView.as_view(), name='all-professor'),
    path('professor/<slug:slug>/', ProfessorDetailView.as_view(), name='professor')
]
