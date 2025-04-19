from django.contrib import admin
from .models import Client, Message, Mailing, MailingAttempt
from django.contrib.auth import get_user_model

User = get_user_model()


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', 'owner')
    list_filter = ('owner',)
    search_fields = ('email', 'full_name')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'owner')
    list_filter = ('owner',)
    search_fields = ('subject', 'body')


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('id', 'start_time', 'end_time', 'status', 'message', 'owner')
    list_filter = ('status', 'owner')
    filter_horizontal = ('clients',)
    date_hierarchy = 'start_time'


@admin.register(MailingAttempt)
class MailingAttemptAdmin(admin.ModelAdmin):
    list_display = ('mailing', 'attempt_time', 'status', 'server_response')
    list_filter = ('status', 'mailing__owner')
    readonly_fields = ('attempt_time',)
    date_hierarchy = 'attempt_time'


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_blocked')
    list_filter = ('is_staff', 'is_blocked')
    search_fields = ('email', 'first_name', 'last_name')
    actions = ['block_users', 'unblock_users']

    def block_users(self, request, queryset):
        queryset.update(is_blocked=True)
        self.message_user(request, "Выбранные пользователи заблокированы")
    block_users.short_description = "Заблокировать выбранных пользователей"

    def unblock_users(self, request, queryset):
        queryset.update(is_blocked=False)
        self.message_user(request, "Выбранные пользователи разблокированы")
    unblock_users.short_description = "Разблокировать выбранных пользователей"
