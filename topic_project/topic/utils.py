from django.core.mail import send_mail
from django.conf import settings
from .models import EmailVerification


def send_verification_email(email: str) -> str:
    verification, created = EmailVerification.objects.update_or_create( email = email, defaults = {"code": EmailVerification.code})
    # to remove the annoying pylance error
    if created:
        pass
    subject = "Your Verification Code for Topic"
    message = f"Your Verification code is: {verification.code}\nThis code expires in 10 minutes.\nThank you for signing up to Topic."
    from_email = settings.EMAIL or "noreply@localhost"
    recipient_list = [email]
    
    send_mail(subject, message, from_email, recipient_list)

    return verification.code
