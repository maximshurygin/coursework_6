from django.core.management.base import BaseCommand
from service.mailing import send_scheduled_emails


class Command(BaseCommand):
    help = 'Отправка рассылок'

    def handle(self, *args, **options):
        send_scheduled_emails()
