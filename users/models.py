from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_blocked = models.BooleanField(default=False, verbose_name='Заблокирован')

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        permissions = [
            ('can_view_all_mailings', 'Может просматривать все рассылки'),
            ('can_view_all_clients', 'Может просматривать всех клиентов'),
            ('can_block_users', 'Может блокировать пользователей'),
            ('can_disable_mailings', 'Может отключать рассылки'),
        ]
