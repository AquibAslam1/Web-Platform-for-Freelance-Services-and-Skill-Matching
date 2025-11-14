from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import FreelancerProfile, RecruiterProfile

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=5)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']

    def create(self, data):
        return User.objects.create_user(
            username=data['username'],
            email=data.get('email'),
            password=data['password'],
            role=data['role']
        )


class FreelancerProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = FreelancerProfile
        fields = [
            'user',
            'headline',
            'summary',
            'education',
            'years_of_experience',
            'tech_stack',
            'skills',
            'dob',
            'resume'
        ]


class RecruiterProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = RecruiterProfile
        fields = ['user', 'company_name', 'website', 'about']


class UserSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'profile']

    def get_profile(self, obj):
        if obj.role == "freelancer" and hasattr(obj, "freelancer_profile"):
            return FreelancerProfileSerializer(obj.freelancer_profile).data
        elif obj.role == "recruiter" and hasattr(obj, "recruiter_profile"):
            return RecruiterProfileSerializer(obj.recruiter_profile).data
        return None
