from django.core.management.base import BaseCommand
from newsletter_app.tasks import send_scheduled_mailings


class Command(BaseCommand):
    help = 'Send scheduled mailings'

    def handle(self, *args, **options):
        self.stdout.write('Starting to send scheduled mailings...')
        send_scheduled_mailings.delay()
        self.stdout.write(self.style.SUCCESS('Successfully started sending mailings'))
