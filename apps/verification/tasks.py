import logging
from celery import shared_task
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from apps.users.models import User
logger = logging.getLogger(__name__)

@shared_task
def send_email_task(user_id,otp):
    user = User.objects.get(id=user_id)
    context = {"user":user,"otp":otp}
    message = render_to_string('otp_email.html', context)

    email = EmailMessage(
        subject="Your OTP Code",
        body=message,
        to=[user.email],
        from_email="no-reply@example.com",
    )
    email.content_subtype = "html"
    email.send(fail_silently=False)

    logger.info("Email send successfull")

