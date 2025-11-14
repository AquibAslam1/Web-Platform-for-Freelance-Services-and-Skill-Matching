from django.contrib import admin
from .models import User, FreelancerProfile, RecruiterProfile

admin.site.register(User)
admin.site.register(FreelancerProfile)
admin.site.register(RecruiterProfile)
