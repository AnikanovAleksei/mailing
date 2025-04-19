from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.core.mail import send_mail
from django.core.cache import cache
from django.http import JsonResponse

from .models import Client, Message, Mailing, MailingAttempt
from .forms import ClientForm, MessageForm, MailingForm, MailingStatusForm
from users.models import User
from .forms import UserBlockForm


class OwnerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        return obj.owner == self.request.user or self.request.user.has_perm('users.can_view_all_mailings')


class ManagerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.has_perm('users.can_view_all_mailings')


class HomeView(ListView):
    template_name = 'mailing/home.html'
    context_object_name = 'mailings'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.has_perm('users.can_view_all_mailings'):
                return Mailing.objects.all()
            return Mailing.objects.filter(owner=self.request.user)
        return Mailing.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        cache_key = 'mailing_stats'
        stats = cache.get(cache_key)

        if not stats:
            total_mailings = Mailing.objects.count()
            active_mailings = Mailing.objects.filter(status=Mailing.STARTED).count()
            unique_clients = Client.objects.values('email').distinct().count()

            stats = {
                'total_mailings': total_mailings,
                'active_mailings': active_mailings,
                'unique_clients': unique_clients,
            }
            cache.set(cache_key, stats, 300)  # Кешируем на 5 минут

        context.update(stats)
        return context


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'mailing/client_list.html'
    context_object_name = 'clients'

    def get_queryset(self):
        if self.request.user.has_perm('users.can_view_all_clients'):
            return Client.objects.all()
        return Client.objects.filter(owner=self.request.user)


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'mailing/client_form.html'
    success_url = reverse_lazy('mailing:client_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, 'Клиент успешно добавлен.')
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, OwnerRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'mailing/client_form.html'
    success_url = reverse_lazy('mailing:client_list')

    def form_valid(self, form):
        messages.success(self.request, 'Клиент успешно обновлен.')
        return super().form_valid(form)


class ClientDeleteView(LoginRequiredMixin, OwnerRequiredMixin, DeleteView):
    model = Client
    template_name = 'mailing/client_confirm_delete.html'
    success_url = reverse_lazy('mailing:client_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Клиент успешно удален.')
        return super().delete(request, *args, **kwargs)


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'mailing/message_list.html'
    context_object_name = 'messages'

    def get_queryset(self):
        return Message.objects.filter(owner=self.request.user)


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailing/message_form.html'
    success_url = reverse_lazy('mailing:message_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, 'Сообщение успешно создано.')
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, OwnerRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailing/message_form.html'
    success_url = reverse_lazy('mailing:message_list')

    def form_valid(self, form):
        messages.success(self.request, 'Сообщение успешно обновлено.')
        return super().form_valid(form)


class MessageDeleteView(LoginRequiredMixin, OwnerRequiredMixin, DeleteView):
    model = Message
    template_name = 'mailing/message_confirm_delete.html'
    success_url = reverse_lazy('mailing:message_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Сообщение успешно удалено.')
        return super().delete(request, *args, **kwargs)


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = 'mailing/mailing_list.html'
    context_object_name = 'mailings'

    def get_queryset(self):
        if self.request.user.has_perm('users.can_view_all_mailings'):
            return Mailing.objects.all()
        return Mailing.objects.filter(owner=self.request.user)


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/mailing_form.html'
    success_url = reverse_lazy('mailing:mailing_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, 'Рассылка успешно создана.')
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, OwnerRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/mailing_form.html'
    success_url = reverse_lazy('mailing:mailing_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, 'Рассылка успешно обновлена.')
        return super().form_valid(form)


class MailingDeleteView(LoginRequiredMixin, OwnerRequiredMixin, DeleteView):
    model = Mailing
    template_name = 'mailing/mailing_confirm_delete.html'
    success_url = reverse_lazy('mailing:mailing_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Рассылка успешно удалена.')
        return super().delete(request, *args, **kwargs)


class MailingDetailView(LoginRequiredMixin, OwnerRequiredMixin, DetailView):
    model = Mailing
    template_name = 'mailing/mailing_detail.html'


class MailingStatusUpdateView(LoginRequiredMixin, ManagerRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingStatusForm
    template_name = 'mailing/mailing_status_form.html'
    success_url = reverse_lazy('mailing:mailing_list')

    def form_valid(self, form):
        messages.success(self.request, 'Статус рассылки успешно обновлен.')
        return super().form_valid(form)


def send_mailing_now(request, pk):
    if not request.user.is_authenticated:
        return redirect('users:login')

    mailing = get_object_or_404(Mailing, pk=pk)

    if not (request.user == mailing.owner or request.user.has_perm('users.can_view_all_mailings')):
        messages.error(request, 'У вас нет прав для отправки этой рассылки.')
        return redirect('mailing:mailing_list')

    try:
        mailing.update_status()
        if mailing.status != Mailing.STARTED:
            messages.error(request, 'Рассылка не может быть отправлена в текущем статусе.')
            return redirect('mailing:mailing_detail', pk=pk)

        success_count = 0
        failure_count = 0

        for client in mailing.clients.all():
            try:
                send_mail(
                    subject=mailing.message.subject,
                    message=mailing.message.body,
                    from_email=None,
                    recipient_list=[client.email],
                    fail_silently=False,
                )
                MailingAttempt.objects.create(
                    mailing=mailing,
                    status=MailingAttempt.SUCCESS,
                    server_response='200 OK',
                )
                success_count += 1
            except Exception as e:
                MailingAttempt.objects.create(
                    mailing=mailing,
                    status=MailingAttempt.FAILURE,
                    server_response=str(e),
                )
                failure_count += 1

        messages.success(
            request,
            f'Рассылка отправлена. Успешно: {success_count}, Неуспешно: {failure_count}'
        )
    except Exception as e:
        messages.error(request, f'Ошибка при отправке рассылки: {str(e)}')

    return redirect('mailing:mailing_detail', pk=pk)


class MailingAttemptListView(LoginRequiredMixin, ListView):
    model = MailingAttempt
    template_name = 'mailing/attempt_list.html'
    context_object_name = 'attempts'

    def get_queryset(self):
        if self.request.user.has_perm('users.can_view_all_mailings'):
            return MailingAttempt.objects.all()
        return MailingAttempt.objects.filter(mailing__owner=self.request.user)


class UserListView(LoginRequiredMixin, ManagerRequiredMixin, ListView):
    model = User
    template_name = 'mailing/user_list.html'
    context_object_name = 'users'


class UserBlockView(LoginRequiredMixin, ManagerRequiredMixin, UpdateView):
    model = User
    form_class = UserBlockForm
    template_name = 'mailing/user_block_form.html'
    success_url = reverse_lazy('mailing:user_list')

    def form_valid(self, form):
        messages.success(self.request, 'Статус пользователя успешно обновлен.')
        return super().form_valid(form)


def mailing_stats(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)

    if request.user.has_perm('users.can_view_all_mailings'):
        mailings = Mailing.objects.all()
    else:
        mailings = Mailing.objects.filter(owner=request.user)

    total_mailings = mailings.count()
    active_mailings = mailings.filter(status=Mailing.STARTED).count()
    completed_mailings = mailings.filter(status=Mailing.COMPLETED).count()

    attempts = MailingAttempt.objects.filter(mailing__in=mailings)
    success_attempts = attempts.filter(status=MailingAttempt.SUCCESS).count()
    failure_attempts = attempts.filter(status=MailingAttempt.FAILURE).count()

    data = {
        'total_mailings': total_mailings,
        'active_mailings': active_mailings,
        'completed_mailings': completed_mailings,
        'success_attempts': success_attempts,
        'failure_attempts': failure_attempts,
    }

    return JsonResponse(data)
