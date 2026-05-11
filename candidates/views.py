from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from jobs.models import Job, JobApplication
from matching.utils import calculate_match_percentage

from .models import CandidateProfile
from .forms import (
    FoundationProfileForm, InterProfileForm,
    OngoingProfileForm, CompletedProfileForm, FinalProfileForm,
    CommerceGradProfileForm,
    EducationFormSet, ExperienceFormSet, AchievementFormSet
)

User = get_user_model()


def get_profile_form_class(user, section=None):
    status = user.ca_status

    if section == 'foundation':
        return FoundationProfileForm, "Foundation Details"
    elif section == 'inter':
        return InterProfileForm, "Intermediate Details"

    if status == 'FOUNDATION':
        return FoundationProfileForm, "Foundation Profile"
    elif status == 'INTERMEDIATE':
        return InterProfileForm, "Articleship Seeker Profile"
    elif status == 'ARTICLE_ONGOING':
        return OngoingProfileForm, "Industrial Training / Transfer Profile"
    elif status == 'ARTICLE_COMPLETED':
        return CompletedProfileForm, "CA Job Seeker Profile"
    elif status == 'FINAL_APPEARED':
        return FinalProfileForm, "CA Final & Career Profile"
    elif status == 'COMMERCE_GRAD':
        return CommerceGradProfileForm, "Commerce Professional Profile"

    return FoundationProfileForm, "Update Profile"


@login_required
def candidate_dashboard(request):
    user = request.user
    profile, created = CandidateProfile.objects.get_or_create(user=user)

    if not profile.is_verified:
        messages.warning(request, "Your account is pending admin approval. You cannot access the dashboard yet.")
        return redirect('candidate:pending_approval')

    completion_percent = profile.get_completion_percentage()
    top_matches = []

    if completion_percent > 20:
        active_jobs = Job.objects.filter(status='active').prefetch_related('skills_required')
        applied_job_ids = JobApplication.objects.filter(candidate=user).values_list('job_id', flat=True)

        for job in active_jobs:
            if job.id in applied_job_ids:
                continue

            match_score, matched_skills, missing_skills = calculate_match_percentage(profile, job)

            if match_score >= 50:
                job.match_score = match_score
                job.matched_skills_list = matched_skills
                job.missing_skills_list = missing_skills
                top_matches.append(job)

        top_matches.sort(key=lambda x: x.match_score, reverse=True)
        top_matches = top_matches[:3]

    context = {
        'user': user,
        'profile': profile,
        'completion_percent': completion_percent,
        'status_display': user.get_ca_status_display(),
        'top_matches': top_matches,
    }
    return render(request, 'candidate_dashboard.html', context)


@login_required
def profile_edit(request, section=None):
    user = request.user
    profile, _ = CandidateProfile.objects.get_or_create(user=user)

    FormClass, title = get_profile_form_class(user, section)

    if request.method == 'POST':
        form = FormClass(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, f"{title} updated successfully!")
            return redirect('candidate:dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = FormClass(instance=profile)

    return render(request, 'profile_form.html', {
        'form': form,
        'title': title,
        'section': section
    })


@login_required
def dynamic_onboarding_view(request):
    user = request.user
    profile, created = CandidateProfile.objects.get_or_create(user=user)

    # ✅ ADDED COMMERCE_GRAD TO FORM MAPPING
    form_mapping = {
        'FOUNDATION': FoundationProfileForm,
        'INTERMEDIATE': InterProfileForm,
        'ARTICLE_ONGOING': OngoingProfileForm,
        'ARTICLE_COMPLETED': CompletedProfileForm,
        'FINAL_APPEARED': FinalProfileForm,
        'COMMERCE_GRAD': CommerceGradProfileForm,
    }

    FormClass = form_mapping.get(user.ca_status, FoundationProfileForm)
    _, section_title = get_profile_form_class(user)

    if request.method == 'POST':
        form = FormClass(request.POST, request.FILES, instance=profile)

        edu_formset = EducationFormSet(request.POST, instance=profile, prefix='educations')
        exp_formset = ExperienceFormSet(request.POST, instance=profile, prefix='experiences')
        ach_formset = AchievementFormSet(request.POST, instance=profile, prefix='achievements')

        if form.is_valid() and edu_formset.is_valid() and exp_formset.is_valid() and ach_formset.is_valid():
            form.save()
            edu_formset.save()
            exp_formset.save()
            ach_formset.save()

            messages.success(request, "Profile details updated successfully!")
            return redirect('candidate:dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = FormClass(instance=profile)
        edu_formset = EducationFormSet(instance=profile, prefix='educations')
        exp_formset = ExperienceFormSet(instance=profile, prefix='experiences')
        ach_formset = AchievementFormSet(instance=profile, prefix='achievements')

    # ✅ ALIGNED CONTEXT VARIABLES WITH YOUR onboarding.html
    context = {
        'profile_form': form,
        'education_formset': edu_formset,
        'experience_formset': exp_formset,
        'achievement_formset': ach_formset,
        'section_title': section_title,
        'current_step': user.get_ca_status_display(),
        'completion_percent': profile.get_completion_percentage()
    }
    return render(request, 'onboarding.html', context)


@login_required
def profile_detail_view(request):
    user = request.user
    profile = user.profile

    if not profile.is_verified:
        messages.warning(request, "Your account is pending admin approval.")
        return redirect('candidate:pending_approval')

    template_name = 'cv_template_professional.html'
    if profile.cv_template_preference == 'academic':
        template_name = 'cv_template_academic.html'

    return render(request, template_name, {
        'user': user,
        'profile': profile,
        'educations': profile.educations.all(),
        'experiences': profile.experiences.all(),
        'achievements': profile.achievements.all(),
        'is_owner': True,
    })


@login_required
def upgrade_status(request):
    user = request.user
    profile, _ = CandidateProfile.objects.get_or_create(user=user)

    if not profile.is_verified:
        messages.warning(request, "Your account is pending admin approval. You cannot upgrade status yet.")
        return redirect('candidate:pending_approval')

    if request.method == 'POST':
        # ✅ COMMERCE GRAD SAFEGUARD
        if user.ca_status == 'COMMERCE_GRAD':
            messages.error(request, "Commerce professionals do not use the CA level-up system.")
            return redirect('candidate:dashboard')

        new_status = request.POST.get('new_status')
        current_status = user.ca_status

        missing_fields = []
        if current_status == 'FOUNDATION':
            if not profile.foundation_year or profile.foundation_attempts is None:
                missing_fields.append("Foundation Passing Year & Attempts")
        elif current_status == 'INTERMEDIATE':
            if profile.inter_attempts_g1 is None and profile.inter_attempts_g2 is None:
                missing_fields.append("Intermediate Group Attempts (G1 or G2)")
            if not profile.preferred_articleship_city:
                missing_fields.append("Preferred Articleship City")
        elif current_status == 'ARTICLE_ONGOING':
            if not profile.articleship_start_date:
                missing_fields.append("Articleship Start Date")
            if not profile.current_firm_city:
                missing_fields.append("Current Firm City")
        elif current_status == 'ARTICLE_COMPLETED':
            if not profile.articleship_end_date:
                missing_fields.append("Articleship Completion Date")

        if missing_fields:
            error_msg = f"Cannot Level Up! Please complete the following details first: {', '.join(missing_fields)}"
            messages.error(request, error_msg)
            return redirect('candidate:onboarding')

        if new_status and new_status != current_status:
            user.ca_status = new_status
            user.save()
            messages.success(request, f"Congratulations! You have moved to the {user.get_ca_status_display()} level.")
            return redirect('candidate:onboarding')

    return redirect('candidate:dashboard')


@login_required
def candidate_public_profile(request, username):
    candidate_user = get_object_or_404(User, username=username)
    profile = get_object_or_404(CandidateProfile, user=candidate_user)

    if not profile.is_verified:
        messages.error(request, "This candidate profile is not active yet.")
        return redirect('index')

    is_employer = getattr(request.user, 'is_firm', False) or getattr(request.user, 'is_corporate', False)
    is_self = request.user == candidate_user

    if not (is_employer or is_self):
        return redirect('index')

    template_name = 'cv_template_professional.html'
    if profile.cv_template_preference == 'academic':
        template_name = 'cv_template_academic.html'

    return render(request, template_name, {
        'user': candidate_user,
        'profile': profile,
        'educations': profile.educations.all(),
        'experiences': profile.experiences.all(),
        'achievements': profile.achievements.all(),
    })


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def pending_approval(request):
    return render(request, 'pending_approval.html')


# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth import logout
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages
# from django.contrib.auth import get_user_model
# from jobs.models import Job, JobApplication
# from matching.utils import calculate_match_percentage
#
# from .models import CandidateProfile
# from .forms import (
#     FoundationProfileForm, InterProfileForm,
#     OngoingProfileForm, CompletedProfileForm, FinalProfileForm,
#     CommerceGradProfileForm,
#     EducationFormSet, ExperienceFormSet, AchievementFormSet
# )
#
# User = get_user_model()
#
#
# def get_profile_form_class(user, section=None):
#     status = user.ca_status
#
#     if section == 'foundation':
#         return FoundationProfileForm, "Foundation Details"
#     elif section == 'inter':
#         return InterProfileForm, "Intermediate Details"
#
#     if status == 'FOUNDATION':
#         return FoundationProfileForm, "Foundation Profile"
#     elif status == 'INTERMEDIATE':
#         return InterProfileForm, "Articleship Seeker Profile"
#     elif status == 'ARTICLE_ONGOING':
#         return OngoingProfileForm, "Industrial Training / Transfer Profile"
#     elif status == 'ARTICLE_COMPLETED':
#         return CompletedProfileForm, "CA Job Seeker Profile"
#     elif status == 'FINAL_APPEARED':
#         return FinalProfileForm, "CA Final & Career Profile"
#     elif status == 'COMMERCE_GRAD':
#         return CommerceGradProfileForm, "Commerce Professional Profile"
#
#     return FoundationProfileForm, "Update Profile"
#
#
# @login_required
# def candidate_dashboard(request):
#     user = request.user
#     profile, created = CandidateProfile.objects.get_or_create(user=user)
#
#     if not profile.is_verified:
#         messages.warning(request, "Your account is pending admin approval. You cannot access the dashboard yet.")
#         return redirect('candidate:pending_approval')
#
#     completion_percent = profile.get_completion_percentage()
#     top_matches = []
#
#     if completion_percent > 20:
#         active_jobs = Job.objects.filter(status='active').prefetch_related('skills_required')
#         applied_job_ids = JobApplication.objects.filter(candidate=user).values_list('job_id', flat=True)
#
#         for job in active_jobs:
#             if job.id in applied_job_ids:
#                 continue
#
#             match_score, matched_skills, missing_skills = calculate_match_percentage(profile, job)
#
#             if match_score >= 50:
#                 job.match_score = match_score
#                 job.matched_skills_list = matched_skills
#                 job.missing_skills_list = missing_skills
#                 top_matches.append(job)
#
#         top_matches.sort(key=lambda x: x.match_score, reverse=True)
#         top_matches = top_matches[:3]
#
#     context = {
#         'user': user,
#         'profile': profile,
#         'completion_percent': completion_percent,
#         'status_display': user.get_ca_status_display(),
#         'top_matches': top_matches,
#     }
#     return render(request, 'candidate_dashboard.html', context)
#
#
# @login_required
# def profile_edit(request, section=None):
#     user = request.user
#     profile, _ = CandidateProfile.objects.get_or_create(user=user)
#
#     FormClass, title = get_profile_form_class(user, section)
#
#     if request.method == 'POST':
#         form = FormClass(request.POST, request.FILES, instance=profile)
#         if form.is_valid():
#             form.save()
#             messages.success(request, f"{title} updated successfully!")
#             return redirect('candidate:dashboard')
#         else:
#             messages.error(request, "Please correct the errors below.")
#     else:
#         form = FormClass(instance=profile)
#
#     return render(request, 'profile_form.html', {
#         'form': form,
#         'title': title,
#         'section': section
#     })
#
#
# @login_required
# def dynamic_onboarding_view(request):
#
#     user = request.user
#     profile, created = CandidateProfile.objects.get_or_create(user=user)
#
#     form_mapping = {
#         'FOUNDATION': FoundationProfileForm,
#         'INTERMEDIATE': InterProfileForm,
#         'ARTICLE_ONGOING': OngoingProfileForm,
#         'ARTICLE_COMPLETED': CompletedProfileForm,
#         'FINAL_APPEARED': FinalProfileForm,
#     }
#
#     FormClass = form_mapping.get(user.ca_status, FoundationProfileForm)
#
#     if request.method == 'POST':
#         form = FormClass(request.POST, request.FILES, instance=profile)
#
#         edu_formset = EducationFormSet(request.POST, instance=profile)
#         exp_formset = ExperienceFormSet(request.POST, instance=profile)
#         ach_formset = AchievementFormSet(request.POST, instance=profile)
#
#         if form.is_valid() and edu_formset.is_valid() and exp_formset.is_valid() and ach_formset.is_valid():
#             form.save()
#             edu_formset.save()
#             exp_formset.save()
#             ach_formset.save()
#
#             messages.success(request, "Profile details updated successfully!")
#             return redirect(
#                 'candidate:dashboard')
#         else:
#             messages.error(request, "Please correct the errors below.")
#     else:
#         form = FormClass(instance=profile)
#         edu_formset = EducationFormSet(instance=profile)
#         exp_formset = ExperienceFormSet(instance=profile)
#         ach_formset = AchievementFormSet(instance=profile)
#
#     context = {
#         'form': form,
#         'edu_formset': edu_formset,
#         'exp_formset': exp_formset,
#         'ach_formset': ach_formset,
#         'current_step': user.get_ca_status_display(),
#         'completion_percent': profile.get_completion_percentage()
#     }
#     return render(request, 'onboarding.html', context)
#
#
# @login_required
# def profile_detail_view(request):
#     user = request.user
#     profile = user.profile
#
#     if not profile.is_verified:
#         messages.warning(request, "Your account is pending admin approval.")
#         return redirect('candidate:pending_approval')
#
#     template_name = 'cv_template_professional.html'
#     if profile.cv_template_preference == 'academic':
#         template_name = 'cv_template_academic.html'
#
#     return render(request, template_name, {
#         'user': user,
#         'profile': profile,
#         'educations': profile.educations.all(),
#         'experiences': profile.experiences.all(),
#         'achievements': profile.achievements.all(),
#         'is_owner': True,
#     })
#
#
# @login_required
# def upgrade_status(request):
#     user = request.user
#     profile, _ = CandidateProfile.objects.get_or_create(user=user)
#
#     if not profile.is_verified:
#         messages.warning(request, "Your account is pending admin approval. You cannot upgrade status yet.")
#         return redirect('candidate:pending_approval')
#
#     if request.method == 'POST':
#         new_status = request.POST.get('new_status')
#         current_status = user.ca_status
#
#         missing_fields = []
#         if current_status == 'FOUNDATION':
#             if not profile.foundation_year or profile.foundation_attempts is None:
#                 missing_fields.append("Foundation Passing Year & Attempts")
#         elif current_status == 'INTERMEDIATE':
#             if profile.inter_attempts_g1 is None and profile.inter_attempts_g2 is None:
#                 missing_fields.append("Intermediate Group Attempts (G1 or G2)")
#             if not profile.preferred_articleship_city:
#                 missing_fields.append("Preferred Articleship City")
#         elif current_status == 'ARTICLE_ONGOING':
#             if not profile.articleship_start_date:
#                 missing_fields.append("Articleship Start Date")
#             if not profile.current_firm_city:
#                 missing_fields.append("Current Firm City")
#         elif current_status == 'ARTICLE_COMPLETED':
#             if not profile.articleship_end_date:
#                 missing_fields.append("Articleship Completion Date")
#
#         if missing_fields:
#             error_msg = f"Cannot Level Up! Please complete the following details first: {', '.join(missing_fields)}"
#             messages.error(request, error_msg)
#             return redirect('candidate:onboarding')
#
#         if new_status and new_status != current_status:
#             user.ca_status = new_status
#             user.save()
#             messages.success(request, f"Congratulations! You have moved to the {user.get_ca_status_display()} level.")
#             return redirect('candidate:onboarding')
#
#     return redirect('candidate:dashboard')
#
#
# @login_required
# def candidate_public_profile(request, username):
#     candidate_user = get_object_or_404(User, username=username)
#     profile = get_object_or_404(CandidateProfile, user=candidate_user)
#
#     if not profile.is_verified:
#         messages.error(request, "This candidate profile is not active yet.")
#         return redirect('index')
#
#     is_employer = getattr(request.user, 'is_firm', False) or getattr(request.user, 'is_corporate', False)
#     is_self = request.user == candidate_user
#
#     if not (is_employer or is_self):
#         return redirect('index')
#
#     template_name = 'cv_template_professional.html'
#     if profile.cv_template_preference == 'academic':
#         template_name = 'cv_template_academic.html'
#
#     return render(request, template_name, {
#         'user': candidate_user,
#         'profile': profile,
#         'educations': profile.educations.all(),
#         'experiences': profile.experiences.all(),
#         'achievements': profile.achievements.all(),
#     })
#
#
# def logout_view(request):
#     logout(request)
#     return redirect('login')
#
#
# @login_required
# def pending_approval(request):
#     return render(request, 'pending_approval.html')
