from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import (
    RegisterSerializer,
    UserSerializer,
    FreelancerProfileSerializer,
    RecruiterProfileSerializer
)
from .models import FreelancerProfile, RecruiterProfile

User = get_user_model()


# ---------------- AUTH ----------------
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        data = UserSerializer(user).data
        if user.role == 'freelancer':
            data['profile'] = FreelancerProfileSerializer(user.freelancer_profile).data
        elif user.role == 'recruiter':
            data['profile'] = RecruiterProfileSerializer(user.recruiter_profile).data
        return Response(data)


# ---------------- PROFILE UPDATE ----------------
class FreelancerProfileUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = FreelancerProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return FreelancerProfile.objects.get(user=self.request.user)


class RecruiterProfileUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = RecruiterProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return RecruiterProfile.objects.get(user=self.request.user)


# ---------------- TEMPLATE RENDER ----------------
def edit_profile(request):
    """Render the profile editing page (frontend form)."""
    return render(request, "edit_profile.html")
