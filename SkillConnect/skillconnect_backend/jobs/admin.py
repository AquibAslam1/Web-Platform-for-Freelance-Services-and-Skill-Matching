from django.contrib import admin
from .models import Job, Application, Favorite, Notification


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'recruiter', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'description', 'tech_stack')


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'job', 'freelancer', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('job__title', 'freelancer__username')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'job', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'job__title')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'message', 'read', 'created_at')
    list_filter = ('read', 'created_at')
    search_fields = ('user__username', 'message')
