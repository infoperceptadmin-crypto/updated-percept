from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from adminpanel.models import ManageSkill, Domain
from .choices import (
    LanguageChoices,
    IndustryChoices,
    DomainChoices,
    JobRoleChoices,
    EmploymentTypeChoices,
    ProficiencyChoices,
    SeekingTypeChoices,
    CareerPreferenceChoices,
    StudyStatusChoices
)


# ==========================================
# 1. MAIN CANDIDATE PROFILE (The Hub)
# ==========================================
class CandidateProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )

    # Professional Summary / Career Objective
    bio = models.TextField(
        blank=True,
        null=True,
        verbose_name="Professional Summary / Objective",
        help_text="A short summary highlighting experience or academic goals."
    )

    # CV Template Preference
    CV_TEMPLATE_CHOICES = [
        ('professional', 'Format A: Professional (Experience-Focused)'),
        ('academic', 'Format B: Fresher (Academic-Focused)'),
    ]
    cv_template_preference = models.CharField(
        max_length=20,
        choices=CV_TEMPLATE_CHOICES,
        default='professional',
        verbose_name="CV Template Format"
    )

    # COMMON / IDENTITY
    icai_reg_num = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="ICAI Registration Number"
    )

    languages = models.JSONField(
        default=list,
        blank=True,
        verbose_name="Languages Known"
    )

    availability = models.CharField(
        max_length=20,
        choices=[
            ('IMMEDIATE', 'Immediate'),
            ('15_DAYS', '15 Days'),
            ('30_DAYS', '30 Days'),
            ('NOTICE', 'Notice Period')
        ],
        blank=True
    )

    # FOUNDATION
    foundation_year = models.PositiveIntegerField(null=True, blank=True)
    foundation_attempts = models.PositiveIntegerField(null=True, blank=True)

    # INTERMEDIATE
    inter_attempts_g1 = models.PositiveIntegerField(null=True, blank=True)
    inter_attempts_g2 = models.PositiveIntegerField(null=True, blank=True)
    preferred_articleship_city = models.CharField(max_length=100, blank=True)

    preferred_industries = models.JSONField(
        default=list,
        blank=True,
        verbose_name="Preferred Industries"
    )

    industry_preference = models.CharField(
        max_length=50,
        choices=IndustryChoices.choices,
        blank=True
    )

    # PREFERRED DOMAINS
    preferred_domains = models.ManyToManyField(
        Domain,
        blank=True,
        related_name='candidates_preferred'
    )

    # ARTICLESHIP ONGOING
    current_firm_city = models.CharField(max_length=100, blank=True)
    articleship_start_date = models.DateField(null=True, blank=True)

    seeking_type = models.CharField(
        max_length=20,
        choices=SeekingTypeChoices.choices,
        blank=True
    )

    is_confidential_mode = models.BooleanField(default=True)

    # ARTICLESHIP COMPLETED
    articleship_end_date = models.DateField(null=True, blank=True)

    domain_exposure = models.JSONField(
        blank=True,
        null=True,
        help_text="Domain-wise exposure with proficiency"
    )

    preferred_job_roles = models.CharField(
        max_length=50,
        choices=JobRoleChoices.choices,
        blank=True
    )

    employment_type = models.CharField(
        max_length=20,
        choices=EmploymentTypeChoices.choices,
        blank=True
    )

    # CA FINAL APPEARED
    final_group_appeared = models.CharField(
        max_length=10,
        choices=[('G1', 'G1'), ('G2', 'G2'), ('BOTH', 'Both')],
        blank=True
    )

    final_attempts = models.PositiveIntegerField(null=True, blank=True)

    career_preference = models.CharField(
        max_length=30,
        choices=CareerPreferenceChoices.choices,
        blank=True
    )

    study_status = models.CharField(
        max_length=20,
        choices=StudyStatusChoices.choices,
        blank=True
    )

    # SKILLS & FILES
    software_skills = models.ManyToManyField(
        ManageSkill,
        through='CandidateSkill',
        blank=True,
        related_name='candidates'
    )

    articleship_completion_cert = models.FileField(
        upload_to='certificates/',
        blank=True,
        null=True
    )

    experience_proof = models.FileField(
        upload_to='experience_proofs/',
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    # ==========================================
    # ADMIN VERIFICATION FIELDS
    # ==========================================
    VERIFICATION_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ]
    status = models.CharField(
        max_length=20,
        choices=VERIFICATION_STATUS_CHOICES,
        default='pending'
    )
    is_verified = models.BooleanField(default=False)

    def clean(self):
        if not self.user_id:
            return

        ca_status = getattr(self.user, 'ca_status', None)
        mandatory_stages = ['ARTICLE_ONGOING', 'ARTICLE_COMPLETED', 'FINAL_APPEARED']

        if ca_status in mandatory_stages and not self.icai_reg_num:
            raise ValidationError({
                'icai_reg_num': "ICAI Registration Number is mandatory for your current CA Status."
            })

        if ca_status == 'ARTICLE_COMPLETED' and not self.articleship_end_date:
            raise ValidationError({
                'articleship_end_date': "Articleship completion date is required."
            })

    def __str__(self):
        return f"{self.user.email} ({getattr(self.user, 'ca_status', 'N/A')})"

    def get_completion_percentage(self):
        if not self.user_id: return 0

        status = getattr(self.user, 'ca_status', None)
        # fields_to_check = ['icai_reg_num', 'software_skills', 'languages']
        if status == 'COMMERCE_GRAD':
            # Commerce grads don't need ICAI number. We check standard professional fields.
            fields_to_check = ['software_skills', 'languages', 'preferred_job_roles', 'employment_type',
                               'preferred_industries']
        else:
            fields_to_check = ['icai_reg_num', 'software_skills', 'languages']

        if status == 'FOUNDATION':
            fields_to_check += ['foundation_year', 'foundation_attempts']
        elif status == 'INTERMEDIATE':
            fields_to_check += ['inter_attempts_g1', 'preferred_articleship_city', 'preferred_industries']
        elif status == 'ARTICLE_ONGOING':
            fields_to_check += ['articleship_start_date', 'current_firm_city', 'seeking_type']
        elif status == 'ARTICLE_COMPLETED':
            fields_to_check += ['articleship_start_date', 'articleship_end_date', 'domain_exposure', 'preferred_job_roles', 'employment_type']
        elif status == 'FINAL_APPEARED':
            fields_to_check += ['final_group_appeared', 'career_preference']

        filled_count = 0
        for field in fields_to_check:
            value = getattr(self, field, None)
            if hasattr(value, 'all'):
                if value.exists():
                    filled_count += 1
            elif value:
                filled_count += 1

        total_points = len(fields_to_check)

        total_points += 1
        if self.educations.exists():
            filled_count += 1

        if status in ['ARTICLE_ONGOING', 'ARTICLE_COMPLETED', 'FINAL_APPEARED']:
            total_points += 1
            if self.experiences.exists():
                filled_count += 1

        if total_points == 0: return 0
        return int((filled_count / total_points) * 100)

class CandidateSkill(models.Model):
    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE)
    skill = models.ForeignKey(ManageSkill, on_delete=models.CASCADE)
    proficiency = models.CharField(
        max_length=50,
        choices=ProficiencyChoices.choices,
        default=ProficiencyChoices.BEGINNER
    )

    class Meta:
        unique_together = ('candidate', 'skill')


# ==========================================
# 2. RELATIONAL MODELS FOR DYNAMIC CV BUILDER
# ==========================================

class Education(models.Model):
    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name='educations')
    qualification_name = models.CharField(max_length=150, verbose_name="Degree / Qualification (e.g., B.Com, HSC)")
    institution_board = models.CharField(max_length=255, verbose_name="Institution / Board")
    passing_year = models.CharField(max_length=20, verbose_name="Year of Passing")
    score_percentage = models.CharField(max_length=50, verbose_name="Marks / Percentage / CGPA")
    remarks = models.CharField(max_length=255, blank=True, null=True, verbose_name="Remarks (e.g., First Attempt)")

    def __str__(self):
        return f"{self.qualification_name} - {self.candidate.user.email}"


class Experience(models.Model):
    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name='experiences')
    designation = models.CharField(max_length=150, verbose_name="Job Title / Designation")
    company_firm_name = models.CharField(max_length=255, verbose_name="Company / Firm Name")
    location = models.CharField(max_length=150, verbose_name="Location")
    start_date = models.DateField(verbose_name="Start Date")
    end_date = models.DateField(blank=True, null=True, verbose_name="End Date")
    is_currently_working = models.BooleanField(default=False, verbose_name="Currently Working Here")

    description = models.TextField(
        verbose_name="Job Description / Roles & Responsibilities",
        help_text="Write bullet points summarizing your work."
    )

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.designation} at {self.company_firm_name}"


class Achievement(models.Model):
    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name='achievements')
    title = models.CharField(max_length=200, verbose_name="Title (e.g., Transfer Pricing Course, Gold Medalist)")
    issuer_organization = models.CharField(max_length=200, blank=True, null=True, verbose_name="Issuing Organization")
    year = models.CharField(max_length=20, blank=True, null=True, verbose_name="Year")
    description = models.TextField(blank=True, null=True, verbose_name="Short Description")

    def __str__(self):
        return self.title

