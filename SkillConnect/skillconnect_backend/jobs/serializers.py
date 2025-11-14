from rest_framework import serializers
from .models import Job, Application, Favorite, Notification


# ---------------- JOB SERIALIZERS ---------------- #

class JobSerializer(serializers.ModelSerializer):
    recruiter = serializers.StringRelatedField(read_only=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = [
            "id", "title", "description", "tech_stack",
            "pay_per_hour", "experience_level", "image",
            "is_active", "created_at", "updated_at", "recruiter"
        ]

    def get_image(self, obj):
        request = self.context.get("request")
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None


class JobCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = [
            "title", "description", "tech_stack",
            "pay_per_hour", "experience_level", "image", "is_active"
        ]


# ---------------- APPLICATION SERIALIZERS ---------------- #

class ApplicationSerializer(serializers.ModelSerializer):
    job_title = serializers.CharField(source="job.title", read_only=True)
    freelancer = serializers.CharField(source="freelancer.username", read_only=True)

    class Meta:
        model = Application
        fields = [
            "id", "job", "job_title",
            "freelancer", "cover_letter",
            "status", "created_at"
        ]


class ApplicationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ["status"]


# ---------------- FAVORITE SERIALIZERS ---------------- #

class FavoriteSerializer(serializers.ModelSerializer):
    job = JobSerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = ["id", "job", "created_at"]


# ---------------- NOTIFICATION SERIALIZERS ---------------- #

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ["id", "message", "read", "created_at"]
