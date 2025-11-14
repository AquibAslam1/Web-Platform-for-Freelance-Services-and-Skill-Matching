from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render, redirect
from django.conf import settings
from django.conf.urls.static import static
from jobs.views import JobDetailFrontendView  # frontend view

# ----------------- Frontend page views -----------------
def home(request):
    return render(request, "index.html")

def login_page(request):
    return render(request, "login.html")

def register_page(request):
    return render(request, "register.html")

def profile_page(request):
    return render(request, "profile.html")

def edit_profile_page(request):
    return render(request, "edit_profile.html")

# ----------------- Redirect old job_detail URL -----------------
def job_detail_redirect(request):
    job_id = request.GET.get('id')
    if job_id:
        return redirect(f'/jobs/{job_id}/')
    return redirect('/')

# ----------------- URL patterns -----------------
urlpatterns = [
    path('admin/', admin.site.urls),

    # API routes
    path('api/', include('users.urls')),
    path('api/jobs/', include('jobs.urls')),

    # Old URL redirect
    path('job_detail/', job_detail_redirect, name='job_detail_redirect'),

    # Frontend pages
    path('', home, name="home"),
    path('login/', login_page, name="login"),
    path('register/', register_page, name="register"),
    path('profile/', profile_page, name="profile"),
    path('edit_profile/', edit_profile_page, name="edit_profile"),

    path('jobs/post/', lambda r: render(r,'job_post.html'), name='job_post'),
    path('jobs/', lambda r: render(r,'job_list.html'), name='job_list'),

    # ✅ Frontend job detail page
    path('jobs/<int:id>/', JobDetailFrontendView.as_view(), name='job_detail'),

    path('jobs/my-applications/', lambda r: render(r,'my_applications.html'), name='my_applications'),
    path('recruiter/dashboard/', lambda r: render(r,'recruiter_dashboard.html'), name='recruiter_dashboard'),
    path('favorites/', lambda r: render(r,'favorites.html'), name='favorites'),
    path('notifications/', lambda r: render(r,'notifications.html'), name='notifications_page'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
