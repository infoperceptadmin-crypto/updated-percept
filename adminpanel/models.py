from django.db import models


class ManageSkill(models.Model):
    CATEGORY_CHOICES = [
        ('Accounting', 'Accounting'),
        ('Analytics', 'Analytics'),
        ('Taxation', 'Taxation'),
        ('Software', 'Software'),
        ('Other', 'Other'),
    ]

    PROFICIENCY_CHOICES = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Expert', 'Expert'),
    ]

    skill_name = models.CharField(max_length=150, unique=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)

    proficiency = models.CharField(
        max_length=50,
        choices=PROFICIENCY_CHOICES,
        default='Beginner'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.skill_name

# class ManageSkill(models.Model):
#
#     CATEGORY_CHOICES = [
#         ('Accounting', 'Accounting'),
#         ('Analytics', 'Analytics'),
#         ('Taxation', 'Taxation'),
#         ('Software', 'Software'),
#         ('Other', 'Other'),
#     ]
#
#     skill_name = models.CharField(max_length=150, unique=True)
#
#     category = models.CharField(
#         max_length=50,
#         choices=CATEGORY_CHOICES
#     )
#
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return self.skill_name


class Domain(models.Model):

    DOMAIN_CHOICES = [
        ('Statutory Audit', 'Statutory Audit'),
        ('Internal Audit', 'Internal Audit'),
        ('Tax Audit', 'Tax Audit'),
        ('GST Compliance', 'GST Compliance'),
        ('Income Tax Returns', 'Income Tax Returns'),
        ('TDS Returns', 'TDS Returns'),
        ('ROC Filings', 'ROC Filings'),
        ('Transfer Pricing', 'Transfer Pricing'),
        ('Bank Audit', 'Bank Audit'),
    ]

    domain_name = models.CharField(
        max_length=100,
        choices=DOMAIN_CHOICES,
        unique=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.domain_name
