from django.db import models
from django.conf import settings
from adminpanel.models import ManageSkill, Domain

class Job(models.Model):
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    firm = models.ForeignKey('employers.Firm', on_delete=models.CASCADE, null=True, blank=True)
    corporate = models.ForeignKey('employers.Corporate', on_delete=models.CASCADE, null=True, blank=True)

    title = models.CharField(max_length=200, verbose_name="Job Title")

    JOB_TYPE_CHOICES = [
        ('articleship', 'Articleship Training'),
        ('industrial', 'Industrial Training'),
        ('full_time', 'Full-Time Job (Post Qualification)'),
        ('part_time', 'Part-Time / Contract'),
    ]
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, default='full_time')

    domains = models.ManyToManyField(Domain, blank=True, related_name="jobs")

    location = models.CharField(max_length=100)
    joining = models.CharField(max_length=50)
    compensation = models.CharField(max_length=50)

    skills_required = models.ManyToManyField(
        ManageSkill,
        related_name="jobs",
        blank=True
    )

    responsibilities = models.TextField()
    learning_exposure = models.TextField()
    ideal_candidate = models.TextField(help_text="Skills and experience required")
    additional_notes = models.TextField(blank=True, null=True)

    min_skill_match = models.IntegerField(default=0)

    status = models.CharField(
        max_length=20,
        choices=[('active', 'Active'), ('closed', 'Closed')],
        default='active'
    )

    posted_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        org_name = self.firm.name if self.firm else (self.corporate.name if self.corporate else "Unknown")
        return f"{self.title} at {org_name}"


class JobApplication(models.Model):
    STATUS_CHOICES = (
        ('applied', 'Applied'),
        ('shortlisted', 'Shortlisted'),
        ('rejected', 'Rejected'),
    )

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    candidate = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='applied')
    applied_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.candidate.email} -> {self.job.title}"
