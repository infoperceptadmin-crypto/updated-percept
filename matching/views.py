from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from jobs.models import Job, JobApplication
from candidates.models import CandidateProfile
from .utils import calculate_match_percentage


@login_required(login_url="/accounts/login/")
def matched_jobs(request):
    jobs_data = []
    applied_job_ids = []

    try:
        candidate = CandidateProfile.objects.get(user=request.user)

        applied_job_ids = list(
            JobApplication.objects.filter(candidate=request.user)
            .values_list("job_id", flat=True)
        )
    except CandidateProfile.DoesNotExist:
        messages.warning(request, "Please create your profile first to see recommendations.")
        return redirect('candidate:onboarding')

    active_jobs = Job.objects.filter(status='active').prefetch_related('skills_required', 'domains')

    for job in active_jobs:

        match_percentage, matched_set, missing_set = calculate_match_percentage(candidate, job)

        if match_percentage < 40:
            continue

        if match_percentage >= 75:
            status, color, action = "High Match", "success", "Apply Now"
        elif match_percentage >= 50:
            status, color, action = "Moderate Match", "warning", "Apply Now"
        else:
            status, color, action = "Low Match", "danger", "Improve Skills"

        jobs_data.append({
            "id": job.id,
            "title": job.title,
            "company": job.firm.name if job.firm else (job.corporate.name if job.corporate else "Company"),
            "location": job.location,
            "skills": [s.skill_name for s in job.skills_required.all()],
            "matched_skills": list(matched_set),
            "missing_skills": list(missing_set),
            "percentage": match_percentage,
            "status": status,
            "color": color,
            "action": action,
            "already_applied": job.id in applied_job_ids,
        })

    jobs_data.sort(key=lambda x: x['percentage'], reverse=True)

    return render(request, "matching/matched_jobs.html", {"jobs": jobs_data})