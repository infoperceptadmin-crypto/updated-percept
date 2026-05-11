from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from adminpanel.models import Domain, ManageSkill
from .models import JobApplication
from employers.models import Firm, Corporate
from django.shortcuts import render, redirect, get_object_or_404
from candidates.models import CandidateProfile
from matching.utils import calculate_match_percentage
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
from django.shortcuts import render
from .models import Job


def get_current_employer(user):
    firm = Firm.objects.filter(user=user).first()
    if firm:
        return firm, 'firm'

    corporate = Corporate.objects.filter(user=user).first()
    if corporate:
        return corporate, 'corporate'

    return None, None


@login_required
def post_job(request):
    employer, emp_type = get_current_employer(request.user)

    if not employer:
        messages.error(request, "We could not find your employer profile.")
        return redirect('index')

    if getattr(employer, 'status', 'pending').lower() != 'approved':
        messages.error(request, "Your account is pending Admin approval. You cannot post jobs yet.")
        return redirect('company_dashboard')

    if request.method == "POST":

        job = Job(
            posted_by=request.user,
            firm=employer if emp_type == 'firm' else None,
            corporate=employer if emp_type == 'corporate' else None,
            title=request.POST.get('title'),
            job_type=request.POST.get('job_type'),
            location=request.POST.get('location'),
            joining=request.POST.get('joining',''),
            compensation=request.POST.get('compensation'),
            responsibilities=request.POST.get('responsibilities'),
            learning_exposure=request.POST.get('learning_exposure',''),
            ideal_candidate=request.POST.get('ideal_candidate'),
            additional_notes=request.POST.get('additional_notes','')
        )
        job.save()

        job.skills_required.set(request.POST.getlist('skills_required'))
        job.domains.set(request.POST.getlist('domains'))

        messages.success(request, "Job posted successfully!")
        return redirect('manage_jobs')

    domains = Domain.objects.all()
    skills = ManageSkill.objects.all()
    return render(request, 'post_job.html', {'domains': domains, 'skills': skills})


@login_required
def manage_jobs(request):
    employer, emp_type = get_current_employer(request.user)

    if not employer:
        messages.error(request, "Access Denied: No Employer Profile Found.")
        return redirect('index')

    if emp_type == 'firm':
        jobs = Job.objects.filter(firm=employer).order_by('-posted_on')
    else:
        jobs = Job.objects.filter(corporate=employer).order_by('-posted_on')

    return render(request, 'manage_jobs.html', {'jobs': jobs})


@login_required
def edit_job(request, job_id):
    employer, emp_type = get_current_employer(request.user)
    if not employer:
        return redirect('index')

    job = get_object_or_404(Job, id=job_id, firm=employer) if emp_type == 'firm' else get_object_or_404(Job, id=job_id,
                                                                                                        corporate=employer)

    if request.method == "POST":
        job.title = request.POST.get('title')
        job.job_type = request.POST.get('job_type')
        job.location = request.POST.get('location')
        job.compensation = request.POST.get('compensation')
        job.joining = request.POST.get('joining','')
        job.responsibilities = request.POST.get('responsibilities')
        job.learning_exposure = request.POST.get('learning_exposure','')
        job.ideal_candidate = request.POST.get('ideal_candidate')
        job.additional_notes = request.POST.get('additional_notes','')
        job.save()

        job.domains.set(request.POST.getlist('domains'))
        job.skills_required.set(request.POST.getlist('skills_required'))

        messages.success(request, "Job updated successfully!")
        return redirect('manage_jobs')

    domains = Domain.objects.all()
    skills = ManageSkill.objects.all()
    return render(request, 'edit_job.html', {'job': job, 'domains': domains, 'skills': skills})


@login_required
def delete_job(request, job_id):
    employer, emp_type = get_current_employer(request.user)

    if emp_type == 'firm':
        job = get_object_or_404(Job, id=job_id, firm=employer)
    else:
        job = get_object_or_404(Job, id=job_id, corporate=employer)

    if request.method == "POST":
        job.delete()
        messages.success(request, "Job deleted successfully!")
        return redirect('manage_jobs')

    return render(request, 'delete_job.html', {'job': job})


@login_required
def employer_analytics_dashboard(request):
    employer, emp_type = get_current_employer(request.user)

    if not employer:
        if getattr(request.user, 'is_firm', False): return redirect('firm_register')
        if getattr(request.user, 'is_corporate', False): return redirect('corporate_register')
        return redirect('index')

    if emp_type == 'firm':
        jobs = Job.objects.filter(firm=employer)
    elif emp_type == 'corporate':
        jobs = Job.objects.filter(corporate=employer)
    else:
        jobs = Job.objects.none()

    total_jobs = jobs.count()
    total_applicants = JobApplication.objects.filter(job__in=jobs).count()
    shortlisted = JobApplication.objects.filter(job__in=jobs, status='shortlisted').count()
    rejected = JobApplication.objects.filter(job__in=jobs, status='rejected').count()

    context = {
        'total_jobs': total_jobs,
        'total_applicants': total_applicants,
        'shortlisted': shortlisted,
        'rejected': rejected,
        'recent_jobs': jobs[:5]
    }
    return render(request, 'dashboard.html', context)


@login_required
def manage_applicants(request, job_id):
    employer, emp_type = get_current_employer(request.user)
    if not employer:
        return redirect('index')

    if emp_type == 'firm':
        job = get_object_or_404(Job, id=job_id, firm=employer)
    else:
        job = get_object_or_404(Job, id=job_id, corporate=employer)

    applicants = JobApplication.objects.filter(job=job).select_related('candidate').order_by('-applied_on')

    status_filter = request.GET.get('status', 'all')
    if status_filter == 'new':
        applicants = applicants.filter(status='applied')
    elif status_filter == 'shortlisted':
        applicants = applicants.filter(status='shortlisted')
    elif status_filter == 'rejected':
        applicants = applicants.filter(status='rejected')

    counts = {
        'all': JobApplication.objects.filter(job=job).count(),
        'new': JobApplication.objects.filter(job=job, status='applied').count(),
        'shortlisted': JobApplication.objects.filter(job=job, status='shortlisted').count(),
        'rejected': JobApplication.objects.filter(job=job, status='rejected').count(),
    }

    return render(request, 'manage_applicants.html', {
        'job': job,
        'applicants': applicants,
        'counts': counts,
        'current_tab': status_filter
    })


@login_required
def update_application_status(request, app_id, status):
    application = get_object_or_404(JobApplication, id=app_id)
    employer, emp_type = get_current_employer(request.user)

    is_owner = False
    if emp_type == 'firm' and application.job.firm == employer:
        is_owner = True
    elif emp_type == 'corporate' and application.job.corporate == employer:
        is_owner = True

    if not is_owner:
        messages.error(request, "Permission Denied")
        return redirect('manage_jobs')

    if status in ['shortlisted', 'rejected', 'applied']:
        previous_status = application.status
        application.status = status
        application.save()

        if previous_status != status:
            send_status_email(application, status)

        messages.success(request, f"Candidate status updated to {status}.")

    return redirect('manage_applicants', job_id=application.job.id)


def send_status_email(application, status):
    candidate_email = application.candidate.email
    job_title = application.job.title
    employer_name = application.job.firm.name if application.job.firm else application.job.corporate.name

    subject = ""
    message = ""

    if status == 'shortlisted':
        subject = f"Good News! You are Shortlisted for {job_title}"
        message = f"Dear {application.candidate.first_name},\n\nWe are pleased to inform you that your application for \"{job_title}\" at {employer_name} has been shortlisted!"
    elif status == 'rejected':
        subject = f"Update on your application for {job_title}"
        message = f"Dear {application.candidate.first_name},\n\nThank you for your interest in \"{job_title}\" at {employer_name}. After careful consideration, we have decided to move forward with other candidates."

    if subject and message:
        try:
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [candidate_email])
        except Exception as e:
            pass



def browse_jobs(request):
    all_jobs_qs = Job.objects.filter(status='active').select_related('firm', 'corporate').prefetch_related('skills_required', 'domains').order_by('-posted_on')

    search_query = request.GET.get('q', '').strip()
    location_query = request.GET.get('location', '').strip()

    if search_query:
        all_jobs_qs = all_jobs_qs.filter(
            Q(title__icontains=search_query) |
            Q(firm__name__icontains=search_query) |
            Q(corporate__name__icontains=search_query) |
            Q(domains__domain_name__icontains=search_query)
        ).distinct()

    if location_query:
        all_jobs_qs = all_jobs_qs.filter(location__icontains=location_query)

    recommended_jobs = []
    all_jobs_list = []

    if request.user.is_authenticated and hasattr(request.user, 'profile'):
        candidate_profile = request.user.profile

        for job in all_jobs_qs:
            percentage, matched_skills, missing_skills = calculate_match_percentage(candidate_profile, job)

            job.match_score = percentage
            job.matched_skills = matched_skills
            job.missing_skills = missing_skills

            all_jobs_list.append(job)

            if percentage >= 50:
                recommended_jobs.append(job)

        recommended_jobs.sort(key=lambda x: x.match_score, reverse=True)
    else:
        all_jobs_list = list(all_jobs_qs)

    context = {
        'recommended_jobs': recommended_jobs,
        'all_jobs_list': all_jobs_list,
        'total_jobs': len(all_jobs_list),
        'search_query': search_query,
        'location_query': location_query
    }
    return render(request, 'browse_jobs.html', context)

@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    if not hasattr(request.user, 'profile'):
        messages.error(request, "Please complete your profile before applying.")
        return redirect('candidate:onboarding')

    if JobApplication.objects.filter(job=job, candidate=request.user).exists():
        messages.warning(request, "You have already applied for this job.")
        return redirect('browse_jobs')

    JobApplication.objects.create(job=job, candidate=request.user, status='applied')
    messages.success(request, "Application sent! The employer will review your CV.")
    return redirect('browse_jobs')


def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    has_applied = False
    match_score = 0

    if request.user.is_authenticated:
        has_applied = JobApplication.objects.filter(job=job, candidate=request.user).exists()
        if hasattr(request.user, 'profile'):
            match_score, _, _ = calculate_match_percentage(request.user.profile, job)

    return render(request, 'job_detail.html', {
        'job': job,
        'has_applied': has_applied,
        'match_score': match_score
    })

