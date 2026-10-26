from django.core.mail import send_mail
from django.conf import settings

def send_confirmation_email(token):
    send_mail(
        subject="Please confirm your email",
        message=f"Confirm your email with this token: http://localhost:8000/confirm/{token.token}/",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[token.user.email]
    )