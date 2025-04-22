from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Email')
    avatar = models.ImageField(upload_to='users/avatars/', blank=True, null=True)
    phone_number = models.CharField(max_length=15, verbose_name='Номер телефона', blank=True, null=True,
                                    help_text='Введите номер телефона')
    country = models.CharField(max_length=20, verbose_name='Страна', null=True, blank=True, help_text='Укажите страну')
    is_blocked = models.BooleanField(default=False, verbose_name='Заблокирован')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        permissions = [
            ('can_view_all_mailings', 'Может просматривать все рассылки'),
            ('can_view_all_clients', 'Может просматривать всех клиентов'),
            ('can_block_users', 'Может блокировать пользователей'),
            ('can_disable_mailings', 'Может отключать рассылки'),
        ]

    def __str__(self):
        return self.email
