import threading
from django.core.mail import send_mail
from django.conf import settings

def send_async_email(subject, message, recipient_list):
    """
    Helper function to send emails asynchronously using threading.
    This prevents the admin dashboard from freezing while emails are being sent.
    """
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
            print(f"Failed to send email to {recipient_list}: {e}")

    email_thread = threading.Thread(target=_send)
    email_thread.start()


def send_firm_status_email(firm, action):
    email = firm.user.email
    firm_name = firm.name

    if action == "approve":
        subject = "Welcome to CA Connect: Your Firm Account is Approved"
        message = f"""Dear {firm_name} Team,

We are pleased to inform you that your firm's registration on CA Connect has been successfully verified and approved.

You can now log in to your employer dashboard to post articleship vacancies, manage job openings, and connect with top CA talent across the network.

Login here: {settings.SITE_URL if hasattr(settings, 'SITE_URL') else 'http://127.0.0.1:8000'}/accounts/login/

Thank you for choosing CA Connect.

Best Regards,
The CA Connect Admin Team
"""
    elif action == "reject":
        subject = "Update regarding your Firm Registration | CA Connect"
        message = f"""Dear {firm_name} Team,

Thank you for your interest in registering with CA Connect.

After a careful review of your submitted registration details, we regret to inform you that we are unable to approve your firm profile at this time. This may be due to incomplete verification details or criteria mismatches.

If you believe this is an error or wish to provide additional documentation, please reply to this email to reach our support team.

Best Regards,
The CA Connect Admin Team
"""
    else:
        return

    send_async_email(subject, message, [email])


def send_corporate_status_email(corporate, action):
    email = corporate.user.email
    corp_name = corporate.name

    if action == "approve":
        subject = "Welcome to CA Connect: Your Corporate Account is Approved"
        message = f"""Dear {corp_name} Team,

We are delighted to welcome you to CA Connect. Your corporate account registration has been successfully verified and approved.

You now have full access to your corporate dashboard. You may log in to post specific finance, audit, and compliance roles, and begin reviewing applications from qualified Chartered Accountants.

Login here: {settings.SITE_URL if hasattr(settings, 'SITE_URL') else 'http://127.0.0.1:8000'}/accounts/login/

Best Regards,
The CA Connect Admin Team
"""
    elif action == "reject":
        subject = "Update regarding your Corporate Registration | CA Connect"
        message = f"""Dear {corp_name} Team,

Thank you for your interest in sourcing talent through CA Connect.

After reviewing your corporate registration details, we regret to advise that we cannot approve your account at this time. 

If you would like us to reconsider your application or if you need to update your corporate verification documents, please contact our support team.

Best Regards,
The CA Connect Admin Team
"""
    else:
        return

    send_async_email(subject, message, [email])


def send_candidate_status_email(candidate, action):
    email = candidate.user.email
    first_name = candidate.user.first_name if candidate.user.first_name else "Candidate"

    if action == "approve":
        subject = "Profile Approved: Start Your Journey on CA Connect"
        message = f"""Dear {first_name},

Congratulations! Your candidate profile on CA Connect has been successfully reviewed and verified.

Your profile is now active. You can log in to explore job opportunities, apply to leading CA Firms and Corporates, and track your application status directly from your dashboard.

Login here: {settings.SITE_URL if hasattr(settings, 'SITE_URL') else 'http://127.0.0.1:8000'}/accounts/login/

We wish you the very best in your professional journey.

Best Regards,
The CA Connect Admin Team
"""
    elif action == "reject":
        subject = "Action Required: Update on your CA Connect Profile"
        message = f"""Dear {first_name},

Thank you for creating a profile on CA Connect.

During our verification process, we noticed some discrepancies or missing information in your profile, and we are unable to approve it in its current state.

Please log in to your account, review your submitted details (such as ICAI registration or academic attempts), and update your profile. Once updated, we will review it again.

Best Regards,
The CA Connect Admin Team
"""
    else:
        return

    send_async_email(subject, message, [email])