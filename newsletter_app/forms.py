from django import forms
from django.core.exceptions import ValidationError
from .models import Client, Message, Mailing
from django.contrib.auth import get_user_model

User = get_user_model()


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['email', 'full_name', 'comment']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'body']
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }


class MailingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['message'].queryset = Message.objects.filter(owner=user)
            self.fields['clients'].queryset = Client.objects.filter(owner=user)

    class Meta:
        model = Mailing
        fields = ['start_time', 'end_time', 'message', 'clients']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'message': forms.Select(attrs={'class': 'form-control'}),
            'clients': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if start_time and end_time and start_time >= end_time:
            raise ValidationError('Время окончания должно быть позже времени начала')


class MailingStatusForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
        }


class UserBlockForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['is_blocked']
        widgets = {
            'is_blocked': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'is_blocked': 'Заблокировать пользователя',
        }
