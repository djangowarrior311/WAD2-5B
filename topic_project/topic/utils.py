from django.core.mail import send_mail
from django.conf import settings
from .models import EmailVerification
from random import randint


def send_verification_email(email: str) -> str:

    new_code = f"{randint(100000, 999999)}"
    verification, created = EmailVerification.objects.update_or_create( email = email, defaults = {"code": new_code})
    # to remove the annoying pylance error
    if created:
        pass
    subject = "Your Verification Code for Topic"
    message = f"Your Verification code is: {verification.code}\nThis code expires in 10 minutes.\nThank you for signing up to Topic."
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@localhost')
    recipient_list = [email]
    
    send_mail(subject, message, from_email, recipient_list)

    return verification.code
