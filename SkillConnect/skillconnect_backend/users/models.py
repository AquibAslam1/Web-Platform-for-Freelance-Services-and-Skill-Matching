from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ('freelancer', 'Freelancer'),
        ('recruiter', 'Recruiter'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.username} ({self.role})"


class FreelancerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='freelancer_profile')

    headline = models.CharField(max_length=120, blank=True)
    summary = models.TextField(blank=True)
    education = models.TextField(blank=True)
    years_of_experience = models.PositiveIntegerField(null=True, blank=True)
    tech_stack = models.TextField(blank=True)
    skills = models.TextField(blank=True)
    dob = models.DateField(null=True, blank=True)
    resume = models.FileField(upload_to="resumes/", null=True, blank=True)

    def __str__(self):
        return f"FreelancerProfile<{self.user.username}>"


class RecruiterProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='recruiter_profile')

    company_name = models.CharField(max_length=160, blank=True)
    website = models.URLField(blank=True)
    about = models.TextField(blank=True)

    def __str__(self):
        return f"RecruiterProfile<{self.user.username}>"
