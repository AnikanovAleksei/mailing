from django.urls import path
from .views import (
    HomeView,
    ClientListView, ClientCreateView, ClientUpdateView, ClientDeleteView,
    MessageListView, MessageCreateView, MessageUpdateView, MessageDeleteView,
    MailingListView, MailingCreateView, MailingUpdateView, MailingDeleteView,
    MailingDetailView, MailingStatusUpdateView, send_mailing_now,
    MailingAttemptListView, UserListView, UserBlockView, mailing_stats,
)

app_name = 'newsletter_app'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('stats/', mailing_stats, name='stats'),

    # Клиенты
    path('clients/', ClientListView.as_view(), name='client_list'),
    path('clients/add/', ClientCreateView.as_view(), name='client_add'),
    path('clients/<int:pk>/edit/', ClientUpdateView.as_view(), name='client_edit'),
    path('clients/<int:pk>/delete/', ClientDeleteView.as_view(), name='client_delete'),

    # Сообщения
    path('messages/', MessageListView.as_view(), name='message_list'),
    path('messages/add/', MessageCreateView.as_view(), name='message_add'),
    path('messages/<int:pk>/edit/', MessageUpdateView.as_view(), name='message_edit'),
    path('messages/<int:pk>/delete/', MessageDeleteView.as_view(), name='message_delete'),

    # Рассылки
    path('mailings/', MailingListView.as_view(), name='mailing_list'),
    path('mailings/add/', MailingCreateView.as_view(), name='mailing_add'),
    path('mailings/<int:pk>/edit/', MailingUpdateView.as_view(), name='mailing_edit'),
    path('mailings/<int:pk>/delete/', MailingDeleteView.as_view(), name='mailing_delete'),
    path('mailings/<int:pk>/', MailingDetailView.as_view(), name='mailing_detail'),
    path('mailings/<int:pk>/status/', MailingStatusUpdateView.as_view(), name='mailing_status'),
    path('mailings/<int:pk>/send/', send_mailing_now, name='send_mailing_now'),

    # Попытки рассылок
    path('attempts/', MailingAttemptListView.as_view(), name='attempt_list'),

    # Управление пользователями (для менеджеров)
    path('users/', UserListView.as_view(), name='user_list'),
    path('users/<int:pk>/block/', UserBlockView.as_view(), name='user_block'),
]
