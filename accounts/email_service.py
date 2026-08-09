import os
import resend


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

    resend.api_key = os.environ.get("RESEND_API_KEY")

    resend.Emails.send({
        "from": "DriveShare <onboarding@resend.dev>",
        "to": [user.email],
        "subject": subject,
        "text": message,
    })