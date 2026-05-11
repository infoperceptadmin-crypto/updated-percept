from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import User
from .models import CandidateProfile

@receiver(post_save, sender=User)
def create_candidate_profile(sender, instance, created, **kwargs):
    if created and instance.is_candidate:
        CandidateProfile.objects.get_or_create(user=instance)