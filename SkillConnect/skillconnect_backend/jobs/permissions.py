# skillconnect_backend/jobs/permissions.py
from rest_framework.permissions import BasePermission

class IsRecruiter(BasePermission):
    """
    Allow only recruiters (User.role == 'recruiter')
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, 'role', None) == 'recruiter'


class IsFreelancer(BasePermission):
    """
    Allow only freelancers (User.role == 'freelancer')
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, 'role', None) == 'freelancer'
