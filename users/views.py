from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetConfirmView
from django.contrib import messages
from django.contrib.auth import login

from .forms import UserRegisterForm, UserLoginForm, UserPasswordResetForm, UserSetPasswordForm


class UserRegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('mailing:home')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Вы успешно зарегистрировались!')
        login(self.request, self.object)
        return response


class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'users/login.html'

    def form_valid(self, form):
        messages.success(self.request, 'Вы успешно вошли в систему!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Неверный email или пароль.')
        return super().form_invalid(form)


class UserLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.success(request, 'Вы успешно вышли из системы.')
        return super().dispatch(request, *args, **kwargs)


class UserPasswordResetView(PasswordResetView):
    form_class = UserPasswordResetForm
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        messages.success(self.request, 'Инструкции по сбросу пароля отправлены на ваш email.')
        return super().form_valid(form)


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = UserSetPasswordForm
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        messages.success(self.request, 'Ваш пароль успешно изменен.')
        return super().form_valid(form)

