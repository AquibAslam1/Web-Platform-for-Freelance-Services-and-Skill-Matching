from django.apps import AppConfig


class JobsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'jobs'
    verbose_name = "Job Management"

    def ready(self):
        """
        Import signals when the app is ready.
        Useful if we want to send notifications when a job is posted or
        when an application is submitted.
        """
        
