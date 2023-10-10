from celery import shared_task
from django.core.mail import send_mail

from sandbox.settings import EMAIL_HOST_USER


@shared_task()
def email_sender(receiver_email, subject, message):
    print("Sending email..")
    send_mail(
        subject,
        message,
        EMAIL_HOST_USER,
        [receiver_email],
        fail_silently=False,
    )
    print("Email sent successfully")
