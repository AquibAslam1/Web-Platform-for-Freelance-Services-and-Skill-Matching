from django.urls import path
from . import views

urlpatterns = [
    path('', views.JobListCreateView.as_view(), name='jobs_list_create'),
    path('detail/<int:pk>/', views.JobDetailView.as_view(), name='job_detail_api'),

    # Apply & favorite
    path('<int:pk>/apply/', views.JobApplyView.as_view(), name='job_apply'),
    path('<int:pk>/favorite/', views.JobFavoriteToggleView.as_view(), name='job_favorite'),

    # Applications
    path('<int:pk>/applicants/', views.JobApplicantsView.as_view(), name='job_applicants'),
    path('applications/my/', views.MyApplicationsView.as_view(), name='my_applications'),
    path('applications/<int:pk>/update/', views.ApplicationStatusUpdateView.as_view(), name='application_update'),

    # Recruiter jobs
    path('recruiter/my-jobs/', views.RecruiterJobsView.as_view(), name='recruiter_jobs'),

    # Favorites & notifications
    path('favorites/', views.FavoritesListView.as_view(), name='favorites'),
    path('notifications/', views.NotificationListView.as_view(), name='notifications'),
    path('notifications/<int:pk>/read/', views.MarkNotificationReadView.as_view(), name='notif_read'),
]
