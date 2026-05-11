import random
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .models import OTP
import threading


def generate_otp():
    return str(random.randint(100000, 999999))


def send_otp_email(user):
    otp_code = generate_otp()

    OTP.objects.update_or_create(
        user=user,
        defaults={
            'otp_code': otp_code,
            'created_at': timezone.now()
        }
    )

    subject = 'Your OTP Verification Code'
    message = (
        f'Hello {user.full_name},\n\n'
        f'Your OTP is: {otp_code}\n'
        f'This OTP is valid for 5 minutes.\n\n'
        f'If you did not request this, please ignore this email.'
    )

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )


def send_approval_email(user, employer_name, employer_type):
    subject = "Account Approved - CA Connect"

    message = (
        f"Dear {employer_name},\n\n"
        f"Your {employer_type} account has been verified and approved by our admin team.\n\n"
        "You can now log in and access your dashboard to post jobs and manage applicants.\n\n"
        "Login here: http://127.0.0.1:8000/accounts/login/\n\n"
        "Best Regards,\n"
        "Team CA Connect"
    )

    recipient_list = [user.email]

    def _send():
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=recipient_list,
                fail_silently=True,
            )
        except Exception as e:
            print(f"Failed to send approval email to {user.email}: {e}")

    email_thread = threading.Thread(target=_send)
    email_thread.start()