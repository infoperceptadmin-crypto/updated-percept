from candidates.models import CandidateProfile

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, get_user_model
from .models import OTP
from .forms import CandidateRegistrationForm
from .utils import send_otp_email
from django.conf import settings

User = get_user_model()


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard_redirect')

    if request.session.get('admin_login'):
        return redirect('adminpanel:admin_dashboard')

    if request.method == "POST":
        email_or_username = request.POST.get('email')
        password = request.POST.get('password')

        if email_or_username == getattr(settings, 'ADMIN_USERNAME', '') and password == getattr(settings,
                                                                                                'ADMIN_PASSWORD', ''):
            request.session['admin_login'] = True
            messages.success(request, "Welcome back, Admin!")
            return redirect('adminpanel:admin_dashboard')

        try:
            user = User.objects.get(email=email_or_username)
        except User.DoesNotExist:
            messages.error(request, "No account found. Please register.")
            return redirect('login')

        if not user.check_password(password):
            messages.error(request, "Invalid password.")
            return redirect('login')

        send_otp_email(user)
        request.session['otp_user_id'] = user.id

        messages.info(request, "Please enter the OTP sent to your email to login.")
        return redirect('verify_otp')

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    request.session.flush()
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')


def register_candidate(request):
    if request.user.is_authenticated:
        logout(request)

    if request.method == 'POST':
        form = CandidateRegistrationForm(request.POST)
        email = request.POST.get('email')
        existing = User.objects.filter(email=email).first()

        if existing and not existing.is_email_verified:
            send_otp_email(existing)
            request.session['otp_user_id'] = existing.id
            messages.info(request, "Account exists but unverified. OTP resent.")
            return redirect('verify_otp')

        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.email
            user.is_candidate = True
            user.is_active = True
            user.is_email_verified = False

            user.save()

            send_otp_email(user)
            request.session['otp_user_id'] = user.id

            messages.success(request, "Registration successful! OTP sent to email.")
            return redirect('verify_otp')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CandidateRegistrationForm()

    return render(request, 'register.html', {'form': form})


def verify_otp(request):
    user_id = request.session.get('otp_user_id')

    if not user_id:
        messages.error(request, "Session expired. Please login again.")
        return redirect('login')

    if request.method == "POST":
        entered_otp = request.POST.get('otp_input')

        try:
            otp_record = OTP.objects.get(user_id=user_id)

            if otp_record.otp_code == entered_otp and otp_record.is_valid():
                user = otp_record.user

                user.is_email_verified = True
                user.save()

                otp_record.delete()
                del request.session['otp_user_id']

                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                messages.success(request, "Verification Successful!")
                return redirect('dashboard_redirect')

            else:
                messages.error(request, "Invalid or expired OTP.")

        except OTP.DoesNotExist:
            messages.error(request, "OTP expired or invalid. Please resend.")

    return render(request, 'verify_otp.html')


def resend_otp(request):
    user_id = request.session.get('otp_user_id')
    if user_id:
        try:
            user = User.objects.get(id=user_id)
            send_otp_email(user)
            messages.success(request, "OTP resent to your email.")
        except User.DoesNotExist:
            pass
    return redirect('verify_otp')


def dashboard_redirect(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('login')

    if user.is_candidate:
        return redirect('candidate:dashboard')

    elif user.is_firm:
         return redirect('firm_dashboard')

    elif user.is_corporate:
         return redirect('corporate_dashboard')

    elif user.is_superuser:
        return redirect('/admin/')

    return redirect('/')




