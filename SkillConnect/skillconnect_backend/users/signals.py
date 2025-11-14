from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, FreelancerProfile, RecruiterProfile

@receiver(post_save, sender=User)
def create_profiles(sender, instance, created, **kwargs):
    if created:
        if instance.role == 'freelancer':
            FreelancerProfile.objects.create(user=instance)
        elif instance.role == 'recruiter':
            RecruiterProfile.objects.create(user=instance)
