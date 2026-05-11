from django.db import models
from django.conf import settings

# =========================
# FIRM MODEL
# =========================

class Firm(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='firm_profile'
    )

    # Firm Details
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True, null=True)

    phonenumber = models.CharField(max_length=20, blank=True, null=True)

    registration_number = models.CharField(
        max_length=50,
        verbose_name="ICAI Firm Reg No"
    )
    partner_details = models.TextField()
    city_area = models.CharField(max_length=100)

    # Numbers
    no_of_partners = models.PositiveIntegerField()
    no_of_paid_assistants = models.PositiveIntegerField()
    articleship_positions = models.PositiveIntegerField(default=0)
    jobs_available = models.PositiveIntegerField()

    # Specialization
    SPECIALIZATION_CHOICES = [
        ('audit', 'Audit-focused Firm'),
        ('tax', 'Tax-focused Firm'),
        ('gst', 'Taxation (GST)'),
        ('mixed', 'Mixed Practice'),
        ('corp_adv', 'Corporate Advisory Firm'),
        ('startup', 'Startup Advisory Firm'),
        ('ma', 'M & A (Mergers & Acquisitions)'),
    ]
    specialization = models.CharField(max_length=200)

    # Exposure & Work
    EXPOSURE_CHOICES = [
        ('High', 'High'),
        ('Moderate', 'Moderate'),
        ('Routine', 'Routine'),
    ]
    exposure_level = models.CharField(
        max_length=10,
        choices=EXPOSURE_CHOICES
    )

    WORK_HOURS_CHOICES = [
        ('Fixed', 'Fixed'),
        ('Seasonal', 'Seasonal Extended'),
    ]
    work_hours = models.CharField(
        max_length=20,
        choices=WORK_HOURS_CHOICES
    )

    # Policy
    stipend_range = models.CharField(max_length=100)
    leave_policy = models.TextField()
    mentorship_available = models.BooleanField(default=True)

    # Approval Flow
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


# =========================
# CORPORATE MODEL
# =========================

class Corporate(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='corporate_profile'
    )

    name = models.CharField(max_length=200)
    address = models.TextField(blank=True, null=True)
    phonenumber = models.CharField(max_length=20, blank=True, null=True)

    registration_number = models.CharField(max_length=50, blank=True, null=True)
    city_area = models.CharField(max_length=200)

    industry_domains_list = models.JSONField(default=list, blank=True)
    finance_exposure = models.JSONField(default=list, blank=True)

    hiring_type = models.CharField(max_length=100, blank=True)
    work_model = models.CharField(max_length=50, blank=True)
    jobs_available = models.IntegerField(blank=True, null=True)

    about = models.TextField(blank=True)

    ca_hiring = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return self.name


    def __str__(self):
        return self.name
