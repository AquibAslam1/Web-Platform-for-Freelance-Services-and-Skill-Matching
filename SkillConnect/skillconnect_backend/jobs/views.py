from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.views.generic import DetailView

from .models import Job, Application, Favorite, Notification
from .serializers import (
    JobSerializer, JobCreateSerializer,
    ApplicationSerializer, ApplicationUpdateSerializer,
    FavoriteSerializer, NotificationSerializer
)
from .permissions import IsRecruiter, IsFreelancer


# ----------------- Jobs list (GET) and create (POST for recruiters) -----------------
class JobListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        qs = Job.objects.filter(is_active=True)

        # search by id or title
        search = self.request.query_params.get("search")
        if search:
            if search.isdigit():
                qs = qs.filter(id=int(search))
            else:
                qs = qs.filter(title__icontains=search)

        # filter by tech_stack
        tech_stack = self.request.query_params.get("tech_stack")
        if tech_stack:
            qs = qs.filter(tech_stack__icontains=tech_stack)

        # filter by pay rate min/max
        min_pay = self.request.query_params.get("min_pay")
        max_pay = self.request.query_params.get("max_pay")
        if min_pay:
            qs = qs.filter(pay_per_hour__gte=min_pay)
        if max_pay:
            qs = qs.filter(pay_per_hour__lte=max_pay)

        # sort by pay or date
        sort = self.request.query_params.get("sort")
        if sort == "pay_high":
            qs = qs.order_by("-pay_per_hour")
        elif sort == "pay_low":
            qs = qs.order_by("pay_per_hour")
        else:
            qs = qs.order_by("-created_at")

        return qs

    def get_serializer_class(self):
        if self.request.method == "POST":
            return JobCreateSerializer
        return JobSerializer

    def perform_create(self, serializer):
        if getattr(self.request.user, "role", None) != "recruiter":
            raise PermissionDenied("Only recruiters can post jobs.")
        serializer.save(recruiter=self.request.user)


# ----------------- Job retrieve (GET) -----------------
class JobDetailView(generics.RetrieveAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]


# ----------------- Freelancer apply to a job -----------------
class JobApplyView(APIView):
    permission_classes = [IsAuthenticated, IsFreelancer]

    def post(self, request, pk):
        job = get_object_or_404(Job, pk=pk, is_active=True)
        user = request.user
        cover_letter = request.data.get("cover_letter", "")

        app, created = Application.objects.get_or_create(
            job=job, freelancer=user, defaults={"cover_letter": cover_letter}
        )
        if not created:
            return Response(
                {"detail": "You already applied to this job."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # create notification for recruiter
        Notification.objects.create(
            user=job.recruiter,
            message=f"{user.username} applied for your job '{job.title}'."
        )

        return Response(ApplicationSerializer(app).data, status=status.HTTP_201_CREATED)


# ----------------- Favorite toggle -----------------
class JobFavoriteToggleView(APIView):
    permission_classes = [IsAuthenticated, IsFreelancer]

    def post(self, request, pk):
        job = get_object_or_404(Job, pk=pk, is_active=True)
        fav, created = Favorite.objects.get_or_create(user=request.user, job=job)
        if not created:
            fav.delete()
            return Response({"detail": "Removed from favorites."})
        return Response({"detail": "Added to favorites."}, status=status.HTTP_201_CREATED)


# ----------------- My Applications (Freelancer) -----------------
class MyApplicationsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsFreelancer]
    serializer_class = ApplicationSerializer

    def get_queryset(self):
        return Application.objects.filter(freelancer=self.request.user).order_by("-created_at")


# ----------------- Recruiter Jobs -----------------
class RecruiterJobsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsRecruiter]
    serializer_class = JobSerializer

    def get_queryset(self):
        return Job.objects.filter(recruiter=self.request.user).order_by("-created_at")


# ----------------- Recruiter sees job applicants -----------------
class JobApplicantsView(APIView):
    """
    Returns a list of applications for a job with embedded freelancer profile details.
    """
    permission_classes = [IsAuthenticated, IsRecruiter]

    def get(self, request, pk):
        job = get_object_or_404(Job, pk=pk, recruiter=request.user)
        apps = job.applications.select_related("freelancer").order_by("-created_at")

        data = []
        for app in apps:
            profile = getattr(app.freelancer, "freelancer_profile", None)

            resume_url = None
            if profile and getattr(profile, "resume", None):
                try:
                    resume_url = request.build_absolute_uri(profile.resume.url)
                except Exception:
                    resume_url = ""

            data.append({
                "id": app.id,
                "freelancer": app.freelancer.username,
                "cover_letter": app.cover_letter or "",
                "status": app.status,
                "profile": {
                    "headline": getattr(profile, "headline", "") if profile else "",
                    "summary": getattr(profile, "summary", "") if profile else "",
                    "education": getattr(profile, "education", "") if profile else "",
                    "experience": getattr(profile, "years_of_experience", "") if profile else "",
                    "tech_stack": getattr(profile, "tech_stack", "") if profile else "",
                    "skills": getattr(profile, "skills", "") if profile else "",
                    "dob": getattr(profile, "dob", "") if profile else "",
                    "resume": resume_url or "",
                }
            })
        return Response(data)


# ----------------- Recruiter updates application status -----------------
class ApplicationStatusUpdateView(generics.UpdateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationUpdateSerializer
    permission_classes = [IsAuthenticated, IsRecruiter]

    def update(self, request, *args, **kwargs):
        app = get_object_or_404(Application, pk=kwargs["pk"])

        if app.job.recruiter != request.user:
            return Response({"detail": "Not allowed"}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(app, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # notify freelancer (db)
        Notification.objects.create(
            user=app.freelancer,
            message=f"Your application for '{app.job.title}' has been updated to '{serializer.data.get('status')}'."
        )

        # optional email
        try:
            if getattr(settings, "EMAIL_HOST", None) and app.freelancer.email:
                send_mail(
                    subject=f"Application update: {app.job.title}",
                    message=f"Hi {app.freelancer.username}, your application status is now: {app.status}",
                    from_email=getattr(settings, "DEFAULT_FROM_EMAIL", None),
                    recipient_list=[app.freelancer.email],
                    fail_silently=True,
                )
        except Exception:
            pass

        return Response(serializer.data)


# ----------------- Favorites List -----------------
class FavoritesListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsFreelancer]
    serializer_class = FavoriteSerializer

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user).order_by("-created_at")


# ----------------- Notifications List -----------------
class NotificationListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by("-created_at")


# ----------------- Mark Notification as Read -----------------
class MarkNotificationReadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        notif = get_object_or_404(Notification, pk=pk, user=request.user)
        notif.read = True
        notif.save()
        return Response(NotificationSerializer(notif).data)


# ----------------- Frontend job detail view -----------------
class JobDetailFrontendView(DetailView):
    model = Job
    template_name = "job_detail.html"
    context_object_name = "job"
    pk_url_kwarg = 'id'
