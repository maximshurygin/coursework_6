from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from service.models import Newsletter, Log


def should_send(newsletter):
    if newsletter.last_sent_at is None:
        return True

    delta = timezone.now() - newsletter.last_sent_at
    if newsletter.frequency == 'daily' and delta.days >= 1:
        return True
    elif newsletter.frequency == 'weekly' and delta.days >= 7:
        return True
    elif newsletter.frequency == 'monthly' and delta.days >= 30:
        return True

    return False


def send_scheduled_emails():
    current_time = timezone.now().time()
    newsletters = Newsletter.objects.filter(start_time__lte=current_time, end_time__gte=current_time, status='running')

    for newsletter in newsletters:
        if not should_send(newsletter):
            continue

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

            newsletter.last_sent_at = timezone.now()
            newsletter.save()
        except Exception as err:
            Log.objects.create(newsletter=newsletter, status=False, server_response=str(err))
