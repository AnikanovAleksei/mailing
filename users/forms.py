from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(
        label=_('Email'),
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
    )
    password1 = forms.CharField(
        label=_('Пароль'),
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    password2 = forms.CharField(
        label=_('Подтверждение пароля'),
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']


class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(
        label=_('Email'),
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
    )
    password = forms.CharField(
        label=_('Пароль'),
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )


class UserPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label=_('Email'),
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
    )


class UserSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label=_('Новый пароль'),
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    new_password2 = forms.CharField(
        label=_('Подтверждение нового пароля'),
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )


class UserBlockForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['is_blocked']
        widgets = {
            'is_blocked': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'is_blocked': _('Заблокировать пользователя'),
        }


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'phone_number', 'avatar',]
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

