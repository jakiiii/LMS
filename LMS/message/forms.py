from django import forms

from .models import MessageBox


class MessageBoxCreationForms(forms.ModelForm):
    class Meta:
        model = MessageBox
        fields = [
            'subject',
            'body'
        ]
        labels = {
            'subject': 'Subject',
            'body': 'Body'
        }


class AdministrationMessageBoxCreationForms(forms.ModelForm):
    class Meta:
        model = MessageBox
        fields = [
            'user',
            'subject',
            'body'
        ]
        labels = {
            'user': 'Student',
            'subject': 'Subject',
            'body': 'Body'
        }
