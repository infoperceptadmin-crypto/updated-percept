from django.db import models


class DomainChoices(models.TextChoices):
    STAT_AUDIT = 'STAT_AUDIT', 'Statutory Audit'
    INT_AUDIT = 'INT_AUDIT', 'Internal Audit'
    TAX_AUDIT = 'TAX_AUDIT', 'Tax Audit'
    DIRECT_TAX = 'DIRECT_TAX', 'Direct Tax (Income Tax, TDS)'
    INDIRECT_TAX = 'INDIRECT_TAX', 'Indirect Tax (GST)'
    ACCOUNTING = 'ACCOUNTING', 'Accounting & Bookkeeping'
    ROC = 'ROC', 'ROC & Company Law'
    TRANSFER_PRICING = 'TRANSFER_PRICING', 'Transfer Pricing'
    BANK_AUDIT = 'BANK_AUDIT', 'Bank Audit'
    CONCURRENT_AUDIT = 'CONCURRENT_AUDIT', 'Concurrent Audit'
    CORP_FINANCE = 'CORP_FINANCE', 'Corporate Finance'
    INVESTMENT_BANKING = 'INVESTMENT_BANKING', 'Investment Banking'
    MERGERS_ACQ = 'MERGERS_ACQ', 'Mergers & Acquisitions'



class IndustryChoices(models.TextChoices):
    MANUFACTURING = 'MANUFACTURING', 'Manufacturing'
    REAL_ESTATE = 'REAL_ESTATE', 'Real Estate'
    IT_STARTUP = 'IT_STARTUP', 'IT / Startups'
    NBFC_BANK = 'NBFC_BANK', 'NBFC / Banks'
    HOSPITAL_NGO = 'HOSPITAL_NGO', 'Hospitals / NGOs'
    RETAIL = 'RETAIL', 'Trading & Retail'



class JobRoleChoices(models.TextChoices):
    AUDIT_EXEC = 'AUDIT_EXEC', 'Audit Executive'
    ACCOUNTS_EXEC = 'ACCOUNTS_EXEC', 'Accounts Executive'
    TAX_EXEC = 'TAX_EXEC', 'Tax Executive'
    GST_ANALYST = 'GST_ANALYST', 'GST Analyst'
    COMPLIANCE_OFFICER = 'COMPLIANCE_OFFICER', 'Compliance Officer'
    MIS_EXEC = 'MIS_EXEC', 'MIS Executive'
    FINANCE_ANALYST = 'FINANCE_ANALYST', 'Finance Analyst'
    VIRTUAL_ACCOUNTANT = 'VIRTUAL_ACCOUNTANT', 'Virtual Accountant'
    CLIENT_REL_EXEC = 'CLIENT_REL_EXEC', 'Client Relationship Executive'


class EmploymentTypeChoices(models.TextChoices):
    FULL_TIME = 'FULL_TIME', 'Full-time'
    CONTRACT = 'CONTRACT', 'Contractual'
    FREELANCE = 'FREELANCE', 'Freelance'
    PROJECT = 'PROJECT', 'Project-based'


class ProficiencyChoices(models.TextChoices):
    BEGINNER = 'BEGINNER', 'Beginner'
    WORKING = 'WORKING', 'Working Knowledge'
    INDEPENDENT = 'INDEPENDENT', 'Independent Handling'



class LanguageChoices(models.TextChoices):
    ENGLISH = 'ENGLISH', 'English'
    HINDI = 'HINDI', 'Hindi'
    REGIONAL_OTHER = 'REGIONAL_OTHER', 'Regional Language'


class SeekingTypeChoices(models.TextChoices):
    TRANSFER = 'TRANSFER', 'Articleship Transfer'
    INDUSTRIAL = 'INDUSTRIAL', 'Industrial Training'


class CareerPreferenceChoices(models.TextChoices):
    CORPORATE_JOB = 'CORPORATE_JOB', 'Corporate Job'
    PRACTICE_SUPPORT = 'PRACTICE_SUPPORT', 'Practice Support'
    VIRTUAL_ROLE = 'VIRTUAL_ROLE', 'Virtual / Remote Role'


class StudyStatusChoices(models.TextChoices):
    STUDY_WORK = 'STUDY_WORK', 'Studying + Working'
    PAUSED = 'PAUSED', 'Temporarily Paused Attempts'
