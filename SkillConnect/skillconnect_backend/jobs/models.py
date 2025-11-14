from django.db import models
from django.conf import settings


class Job(models.Model):
    """
    Job model for recruiters to post opportunities.
    """
    recruiter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='jobs'
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    tech_stack = models.CharField(max_length=255, blank=True)
    pay_per_hour = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    experience_level = models.CharField(max_length=80, blank=True)
    image = models.ImageField(upload_to='job_images/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} — {self.recruiter.username}"


class Application(models.Model):
    """
    Application model for freelancers applying to jobs.
    """
    STATUS_CHOICES = (
        ('applied', 'Applied'),
        ('shortlisted', 'Shortlisted'),
        ('interview', 'Interview'),
        ('hired', 'Hired'),
        ('rejected', 'Rejected'),
    )

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name='applications'
    )
    freelancer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='applications'
    )
    cover_letter = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='applied')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('job', 'freelancer')

    def __str__(self):
        return f"{self.freelancer.username} -> {self.job.title} ({self.status})"


class Favorite(models.Model):
    """
    Users can save jobs for later.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='favorites'
    )
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name='favorited_by'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'job')

    def __str__(self):
        return f"{self.user.username} fav {self.job.title}"


class Notification(models.Model):
    """
    Notifications for application/job updates.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    message = models.TextField()
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        status = "read" if self.read else "new"
        return f"Notif to {self.user.username} - {status}"
