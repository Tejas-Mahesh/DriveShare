from django.core.mail import send_mail
from django.conf import settings


def send_signup_email(user):
    subject = "🎉 Welcome to DriveShare"

    message = f"""
Hi {user.first_name},

Welcome to DriveShare!

Your account has been created successfully.

You can now login and start exploring cars.

Thank you,
DriveShare Team
"""

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )