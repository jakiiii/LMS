from django.urls import path
from .views import (
    StudentInboxMessageListView,
    StudentSentMessageListView,
    StudentNewMessageCreateView,
    StudentMessageDeleteView,
    StudentMessageDetailView,
    StudentInboxMessageDetailView,
    StudentInboxMessageDeleteView,

    AdministrationMessageInboxListView,
    AdministrationMessageSendListView,
    # AdministrationMessageDetailView,
    administration_message_detail_view,
    AdministrationMessageCreateView,
    AdministrationMessageDeleteView,
)


urlpatterns = [
    path('student/new/message/', StudentNewMessageCreateView.as_view(), name='message-create'),
    path('student/message/inbox/', StudentInboxMessageListView.as_view(), name='message-inbox'),
    path('student/message/inbox/<slug:slug>/', StudentInboxMessageDetailView.as_view(), name='student-inbox-detail'),
    path('student/message/inbox/delete/<slug:slug>/', StudentInboxMessageDeleteView.as_view(), name='student-inbox-delete'),
    path('student/message/sent/', StudentSentMessageListView.as_view(), name='message-sent'),
    path('student/message/<slug:slug>/', StudentMessageDetailView.as_view(), name='student-detail-message'),
    path('student/message/delete/<slug:slug>/', StudentMessageDeleteView.as_view(), name='student-delete-message'),

    path('instructor/message/inbox/', AdministrationMessageInboxListView.as_view(), name='message-admin-inbox'),
    path('instructor/message/send/', AdministrationMessageSendListView.as_view(), name='message-admin-send'),
    # path('instructor/message/<slug:slug>/', AdministrationMessageDetailView.as_view(), name='admin-detail-message'),
    path('instructor/message/<slug:slug>/', administration_message_detail_view, name='admin-detail-message'),
    path('instructor/new/message/', AdministrationMessageCreateView.as_view(), name='message-new'),
    path('instructor/message/delete/<slug:slug>/', AdministrationMessageDeleteView.as_view(), name='delete-message'),
]
