from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.utils import timezone
from service.models import Newsletter, Log


class Command(BaseCommand):
    help = 'Send scheduled newsletters'

    def handle(self, *args, **options):
        current_time = timezone.now().time()
        newsletters = Newsletter.objects.filter(start_time__lte=current_time, end_time__gte=current_time,
                                                status='running')

        for newsletter in newsletters:
            subject = newsletter.message.subject
            body = newsletter.message.body
            recipient_list = [client.email for client in newsletter.recipients.all()]

            try:
                send_mail(
                    subject,
                    body,
                    settings.EMAIL_HOST_USER,
                    recipient_list,
                    fail_silently=False,
                )
                Log.objects.create(newsletter=newsletter, status=True)
            except Exception as err:
                Log.objects.create(newsletter=newsletter, status=False, server_response=str(err))
