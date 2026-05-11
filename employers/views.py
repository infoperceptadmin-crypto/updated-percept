from django.contrib import messages, auth
from .models import Corporate, Firm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.utils import send_otp_email
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, get_object_or_404

User = get_user_model()

# ==========================
# HOME / INDEX
# ==========================
def index(request):
    return render(request, 'index.html')
def pending_approval(request):
    return render(request, 'pending_approval')

# ==========================
# REGISTER CHOICE PAGE
# ==========================
def register_choice(request):
    return render(request, 'register_choice.html')

def firm_register(request):
    if request.method == "POST":

        email = request.POST.get('email')
        password = request.POST.get('password')
        mobile = request.POST.get('mobile_number')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Account with this email already exists.")
            return redirect('firm_register')

        if User.objects.filter(mobile_number=mobile).exists():
            messages.error(request, "This mobile number is already registered.")
            return redirect('firm_register')

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            mobile_number=mobile
        )
        user.username = email
        user.is_firm = True
        user.is_active = True
        user.is_email_verified = False
        user.save()

        specializations = request.POST.getlist('specialization')
        specialization_str = ", ".join(specializations)

        firm = Firm.objects.create(
            user=user,
            name=request.POST.get('name'),
            address=request.POST.get('address'),
            phonenumber=request.POST.get('phonenumber'),
            registration_number=request.POST.get('registration_number'),
            partner_details=request.POST.get('partner_details', ''),
            city_area=request.POST.get('city_area'),

            no_of_partners=int(request.POST.get('no_of_partners') or 0),
            no_of_paid_assistants=int(request.POST.get('no_of_paid_assistants') or 0),
            articleship_positions=int(request.POST.get('articleship_positions') or 0),
            jobs_available=int(request.POST.get('jobs_available') or 0),

            specialization=specialization_str,
            exposure_level=request.POST.get('exposure_level'),
            work_hours=request.POST.get('work_hours'),
            stipend_range=request.POST.get('stipend_range'),
            leave_policy=request.POST.get('leave_policy'),
            mentorship_available=bool(request.POST.get('mentorship_available')),
            status='pending'
        )

        send_otp_email(user)

        messages.success(request, "Firm registered. OTP sent to your email.")
        request.session['otp_user_id'] = user.id
        return redirect('verify_otp')

    return render(request, 'firm_register.html')

# ==========================
# FIRM PROFILE
# ==========================
def firm_profile(request, firm_id):
    firm = get_object_or_404(Firm, id=firm_id)

    return render(request, 'firm_profile.html', {
        'firm': firm
    })


# ==========================
# CORPORATE REGISTRATION
# ==========================

def corporate_register(request):
    if request.method == "POST":

        email = request.POST.get('email')
        password = request.POST.get('password')
        mobile = request.POST.get('mobile_number')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Account with this email already exists.")
            return redirect('corporate_register')

        if User.objects.filter(mobile_number=mobile).exists():
            messages.error(request, "This mobile number is already registered.")
            return redirect('corporate_register')

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            mobile_number=mobile
        )
        user.username = email
        user.is_corporate = True
        user.is_active = True
        user.is_email_verified = False
        user.save()

        corporate = Corporate.objects.create(
            user=user,
            name=request.POST.get('name'),
            address=request.POST.get('address'),
            phonenumber=request.POST.get('phonenumber'),
            registration_number=request.POST.get('registration_number'),
            city_area=request.POST.get('city_area'),
            industry_domains_list=request.POST.getlist('industry_domains'),
            finance_exposure=request.POST.getlist('finance_exposure'),
            hiring_type=request.POST.get('hiring_type'),
            work_model=request.POST.get('work_model'),
            jobs_available=int(request.POST.get('jobs_available') or 0),
            about=request.POST.get('about'),
            ca_hiring=bool(request.POST.get('ca_hiring')),
            status='pending',
            is_verified=False
        )

        send_otp_email(user)

        messages.success(request, "Corporate registered. OTP sent to your email.")
        request.session['otp_user_id'] = user.id
        return redirect('verify_otp')

    return render(request, 'corporate_register.html')

# ==========================
# CORPORATE PROFILE
# ==========================
def corporate_profile(request, corporate_id):
    corporate = get_object_or_404(Corporate, id=corporate_id)

    return render(request, 'corporate_profile.html', {
        'corporate': corporate
    })


@login_required
def firm_dashboard(request):

    user = request.user

    if not getattr(user, 'is_email_verified', True):
        messages.warning(request, "Please verify your email address to proceed.")
        request.session['otp_user_id'] = user.id
        return redirect('verify_otp')

    firm = Firm.objects.filter(user=user).first()

    if not firm:
        return redirect('firm_register')

    if firm.status == 'approved':
        return redirect('company_dashboard')

    elif firm.status == 'rejected':
        return render(request, 'pending_approval.html', {'status': 'rejected'})

    else:
        return render(request, 'pending_approval.html', {'status': 'pending'})


@login_required
def corporate_dashboard(request):

    user = request.user
    if not getattr(user, 'is_email_verified', True):
        messages.warning(request, "Please verify your email address to proceed.")
        request.session['otp_user_id'] = user.id
        return redirect('verify_otp')

    corp = Corporate.objects.filter(user=user).first()

    if not corp:
        return redirect('corporate_register')

    if corp.status == 'approved':
        return redirect('company_dashboard')

    elif corp.status == 'rejected':
        return render(request, 'pending_approval.html', {'status': 'rejected'})

    else:
        return render(request, 'pending_approval.html', {'status': 'pending'})
