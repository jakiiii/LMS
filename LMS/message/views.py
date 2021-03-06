from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, ListView, CreateView, DetailView, DeleteView

from .forms import MessageBoxCreationForms, AdministrationMessageBoxCreationForms, MessageBoxReplayCreationForm

from .models import MessageBox, MessageBoxReplay


# Create your views here.
class StudentNewMessageCreateView(LoginRequiredMixin, CreateView):
    form_class = MessageBoxCreationForms
    template_name = 'message/new-message-view.html'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(StudentNewMessageCreateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Send Message'
        context['student_header'] = 'message-create'
        context['student_navbar'] = 'message-create'
        return context

    def get_login_url(self):
        return reverse('login')

    def get_success_url(self):
        return reverse('message-inbox')


class StudentInboxMessageListView(LoginRequiredMixin, ListView):
    paginate_by = 10
    model = MessageBoxReplay
    context_object_name = 'message_replay_context'
    template_name = 'message/message-inbox-view.html'

    def get_context_data(self, *args, **kwargs):
        context = super(StudentInboxMessageListView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Inbox'
        context['student_header'] = 'student-delete-message'
        context['student_navbar'] = 'student-delete-message'
        return context


class StudentInboxMessageDetailView(LoginRequiredMixin, DetailView):
    model = MessageBoxReplay
    template_name = 'message/inbox-message-student-detail-view.html'

    def get_context_data(self, *args, **kwargs):
        context = super(StudentInboxMessageDetailView, self).get_context_data(*args, **kwargs)
        context['title'] = '{}'.format(self.get_object().msg)
        context['student_header'] = 'student-inbox-detail'
        context['student_navbar'] = 'student-inbox-detail'
        return context


class StudentInboxMessageDeleteView(LoginRequiredMixin, DeleteView):
    model = MessageBoxReplay
    template_name = 'message/delete.html'

    def get_context_data(self, **kwargs):
        context = super(StudentInboxMessageDeleteView, self).get_context_data(**kwargs)
        context['title'] = 'Delete - {}'.format(self.get_object().msg)
        context['student_header'] = 'student-inbox-delete'
        context['student_navbar'] = 'student-inbox-delete'
        return context

    def get_success_url(self):
        return reverse('message-inbox')

    def get_login_url(self):
        return reverse('login')


class StudentSentMessageListView(LoginRequiredMixin, ListView):
    paginate_by = 10
    model = MessageBox
    context_object_name = 'message_context'
    template_name = 'message/message-send-view.html'

    def get_context_data(self, *args, **kwargs):
        context = super(StudentSentMessageListView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Send'
        context['student_header'] = 'message-sent'
        context['student_navbar'] = 'message-sent'
        return context

    def get_queryset(self):
        return MessageBox.objects.filter(user=self.request.user)


class StudentMessageDetailView(LoginRequiredMixin, DetailView):
    model = MessageBox
    template_name = 'message/message-student-detail-view.html'

    def get_context_data(self, *args, **kwargs):
        context = super(StudentMessageDetailView, self).get_context_data(*args, **kwargs)
        context['title'] = '{}'.format(self.get_object().subject)
        context['student_header'] = 'student-delete-message'
        context['student_navbar'] = 'student-delete-message'
        return context


class StudentMessageDeleteView(LoginRequiredMixin, DeleteView):
    model = MessageBox
    template_name = 'message/delete.html'

    def get_context_data(self, *args, **kwargs):
        context = super(StudentMessageDeleteView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Delete - {}'.format(self.get_object().msg)
        context['student_header'] = 'student-delete-message'
        context['student_navbar'] = 'student-delete-message'
        return context

    def get_success_url(self):
        return reverse('message-inbox')

    def get_login_url(self):
        return reverse('login')


'''
------------------------- End Student Message Section ------------------------------------
------------------------- Start Administration Message Section ---------------------------
'''


class AdministrationMessageInboxListView(LoginRequiredMixin, ListView):
    model = MessageBox
    context_object_name = 'all_message_context'
    template_name = 'message/manage-messeve-view.html'

    def get_context_data(self, *args, **kwargs):
        context = super(AdministrationMessageInboxListView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Inbox'
        context['instructor_navbar'] = 'message-admin-inbox'
        return context


class AdministrationMessageSendListView(LoginRequiredMixin, ListView):
    model = MessageBox
    context_object_name = 'self_message_context'
    template_name = 'message/message-admin-send-view.html'

    def get_context_data(self, *args, **kwargs):
        context = super(AdministrationMessageSendListView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Send Message'
        context['instructor_navbar'] = 'message-admin-send'
        return context

    def get_queryset(self):
        return MessageBox.objects.filter(user=self.request.user)


# class AdministrationMessageDetailView(LoginRequiredMixin, DetailView):
#     model = MessageBox
#     template_name = 'message/message-admin-detail-view.html'
#
#     def get_context_data(self, *args, **kwargs):
#         context = super(AdministrationMessageDetailView, self).get_context_data(*args, **kwargs)
#         context['title'] = '{}'.format(self.get_object().subject)
#         context['instructor_navbar'] = 'admin-detail-message'
#         return context


@login_required
def administration_message_detail_view(request, slug):
    msg_obj = MessageBox.objects.get(slug=slug)
    title = 'Message Details'  # '{}'.format(msg_obj.get(subject='subject'))
    template_name = 'message/message-admin-detail-view.html'

    form = MessageBoxReplayCreationForm(request.POST or None)
    if form.is_valid():
        reply = form.cleaned_data.get('reply')
        user = request.user
        message = msg_obj
        MessageBoxReplay.objects.create(user=user, msg=message, reply=reply)
        return HttpResponseRedirect('/instructor/message/inbox')

    context = {
        'instructor_navbar': 'admin-detail-message',
        'title': title,
        'object': msg_obj,
        'form': form
    }
    return render(request, template_name, context)


class AdministrationMessageCreateView(LoginRequiredMixin, CreateView):
    form_class = AdministrationMessageBoxCreationForms
    template_name = 'message/create-messeve-view.html'

    def get_context_data(self, *args, **kwargs):
        context = super(AdministrationMessageCreateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Send'
        context['instructor_navbar'] = 'message-new'
        return context

    # def get_queryset(self):
    #     return MessageBox.objects.all().exclude(user=self.request.user)

    def get_login_url(self):
        return reverse('login')

    def get_success_url(self):
        return reverse('message-admin-send')


class AdministrationMessageDeleteView(LoginRequiredMixin, DeleteView):
    model = MessageBox
    template_name = 'message/delete.html'

    def get_context_data(self, *args, **kwargs):
        context = super(AdministrationMessageDeleteView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Send'
        context['instructor_navbar'] = 'message-delete'
        return context

    def get_success_url(self):
        return reverse('message-admin-inbox')

    def get_login_url(self):
        return reverse('login')


# class MessageReplay(LoginRequiredMixin, CreateView):
#     form_class = MessageBoxReplayCreationForm
#     template_name = 'message/message-admin-detail-view.html'
