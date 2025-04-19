from celery import shared_task
from django.utils import timezone
from django.core.mail import send_mail
from .models import Mailing, MailingAttempt


@shared_task
def send_scheduled_mailings():
    now = timezone.now()
    mailings = Mailing.objects.filter(
        start_time__lte=now,
        end_time__gte=now,
        status__in=[Mailing.CREATED, Mailing.STARTED]
    )

    for mailing in mailings:
        mailing.update_status()
        if mailing.status != Mailing.STARTED:
            continue

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
            except Exception as e:
                MailingAttempt.objects.create(
                    mailing=mailing,
                    status=MailingAttempt.FAILURE,
                    server_response=str(e),
                )
