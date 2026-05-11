from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from datetime import timedelta

class User(AbstractUser):
    is_candidate = models.BooleanField(default=False)
    is_firm = models.BooleanField(default=False)
    is_corporate = models.BooleanField(default=False)

    full_name = models.CharField(max_length=255, verbose_name="Full Name")
    email = models.EmailField(unique=True, verbose_name="Email ID")
    mobile_number = models.CharField(max_length=15, unique=True, verbose_name="Mobile Number")
    is_email_verified = models.BooleanField(default=False)
    city = models.CharField(max_length=100, verbose_name="Preferred Work Location")

    class CAStatus(models.TextChoices):
        FOUNDATION_CLEARED = 'FOUNDATION', 'CA Foundation Cleared'
        INTERMEDIATE = 'INTERMEDIATE', 'CA Intermediate'
        ARTICLESHIP_ONGOING = 'ARTICLE_ONGOING', 'Articleship Ongoing'
        ARTICLESHIP_COMPLETED = 'ARTICLE_COMPLETED', 'Articleship Completed'
        FINAL_APPEARED = 'FINAL_APPEARED', 'CA Final Appeared / Not Cleared'
        COMMERCE_GRAD = 'COMMERCE_GRAD', 'Commerce Graduate / Post-Graduate'

    ca_status = models.CharField(
        max_length=20,
        choices=CAStatus.choices,
        verbose_name="Current CA Status",
        blank=True,
        null=True
    )

    class InterGroupStatus(models.TextChoices):
        G1 = 'G1', 'Group 1 Cleared'
        G2 = 'G2', 'Group 2 Cleared'
        BOTH = 'BOTH', 'Both Groups Cleared'

    inter_group_status = models.CharField(
        max_length=10,
        choices=InterGroupStatus.choices,
        blank=True,
        null=True,
        verbose_name="Intermediate Groups Cleared"
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'full_name', 'mobile_number']

    def __str__(self):
        return self.email

class OTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(default=timezone.now)

    def is_valid(self):
        return timezone.now() < self.created_at + timedelta(minutes=5)

    def __str__(self):
        return f"OTP for {self.user.email}"