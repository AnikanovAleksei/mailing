from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.validators import EmailValidator

User = get_user_model()


class Client(models.Model):
    email = models.EmailField(unique=True, validators=[EmailValidator()])
    full_name = models.CharField(max_length=255, verbose_name='ФИО')
    comment = models.TextField(blank=True, verbose_name='Комментарий')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Владелец')

    def __str__(self):
        return f'{self.full_name} ({self.email})'

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'


class Message(models.Model):
    subject = models.CharField(max_length=255, verbose_name='Тема письма')
    body = models.TextField(verbose_name='Тело письма')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Владелец')

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'


class Mailing(models.Model):
    CREATED = 'created'
    STARTED = 'started'
    COMPLETED = 'completed'

    STATUS_CHOICES = [
        (CREATED, 'Создана'),
        (STARTED, 'Запущена'),
        (COMPLETED, 'Завершена'),
    ]

    start_time = models.DateTimeField(verbose_name='Время начала рассылки')
    end_time = models.DateTimeField(verbose_name='Время окончания рассылки')
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=CREATED,
        verbose_name='Статус'
    )
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        verbose_name='Сообщение'
    )
    clients = models.ManyToManyField(Client, verbose_name='Клиенты')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Владелец')

    def __str__(self):
        return f'Рассылка #{self.pk} ({self.get_status_display()})'

    def update_status(self):
        now = timezone.now()
        if self.status == self.CREATED and self.start_time <= now <= self.end_time:
            self.status = self.STARTED
            self.save()
        elif self.status == self.STARTED and now > self.end_time:
            self.status = self.COMPLETED
            self.save()

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'
        ordering = ['-start_time']


class MailingAttempt(models.Model):
    SUCCESS = 'success'
    FAILURE = 'failure'

    STATUS_CHOICES = [
        (SUCCESS, 'Успешно'),
        (FAILURE, 'Не успешно'),
    ]

    attempt_time = models.DateTimeField(auto_now_add=True, verbose_name='Время попытки')
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        verbose_name='Статус попытки'
    )
    server_response = models.TextField(blank=True, verbose_name='Ответ сервера')
    mailing = models.ForeignKey(
        Mailing,
        on_delete=models.CASCADE,
        related_name='attempts',
        verbose_name='Рассылка'
    )

    def __str__(self):
        return f'Попытка рассылки #{self.pk} ({self.get_status_display()})'

    class Meta:
        verbose_name = 'попытка рассылки'
        verbose_name_plural = 'попытки рассылки'
        ordering = ['-attempt_time']
