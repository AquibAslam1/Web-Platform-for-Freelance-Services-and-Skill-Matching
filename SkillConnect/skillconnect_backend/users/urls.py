from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views   

urlpatterns = [
    # -------- AUTH --------
    path("auth/register/", views.RegisterView.as_view(), name="register"),
    path("auth/login/", TokenObtainPairView.as_view(), name="login"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # -------- USER --------
    path("me/", views.MeView.as_view(), name="me"),

    # -------- PROFILE --------
    path("freelancer/profile/", views.FreelancerProfileUpdateView.as_view(), name="freelancer_profile"),
    path("recruiter/profile/", views.RecruiterProfileUpdateView.as_view(), name="recruiter_profile"),

    # -------- TEMPLATE --------
    path("edit_profile/", views.edit_profile, name="edit_profile"),
]
