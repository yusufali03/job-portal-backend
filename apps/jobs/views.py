from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, generics
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.permissions import IsEmployerOwnerOrReadOnly, IsEmployerRole

from .models import Job
from .serializers import (
    JobCreateUpdateSerializer,
    JobDetailSerializer,
    JobListSerializer, EmployerDashboardSummarySerializer,
)
from ..applications.models import Application


class JobListCreateView(ListCreateAPIView):
    queryset = Job.objects.select_related("employer").all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["category", "location", "job_type", "status"]
    search_fields = ["title", "description", "requirements", "location", "category"]
    ordering_fields = ["created_at", "salary", "application_deadline"]
    ordering = ["-created_at"]

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAuthenticated(), IsEmployerRole()]
        return [permissions.AllowAny()]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return JobCreateUpdateSerializer
        return JobListSerializer


class JobRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Job.objects.select_related("employer").all()

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny()]
        return [
            permissions.IsAuthenticated(),
            IsEmployerRole(),
            IsEmployerOwnerOrReadOnly(),
        ]

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return JobCreateUpdateSerializer
        return JobDetailSerializer

class EmployerJobListView(generics.ListAPIView):
    serializer_class = JobListSerializer
    permission_classes = [permissions.IsAuthenticated, IsEmployerRole]

    def get_queryset(self):
        return Job.objects.select_related("employer").filter(
            employer=self.request.user
        ).order_by("-created_at")


class EmployerDashboardSummaryView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsEmployerRole]

    def get(self, request):
        employer = request.user

        jobs_queryset = Job.objects.filter(employer=employer)
        applications_queryset = Application.objects.filter(job__employer=employer)

        summary_data = {
            "total_jobs": jobs_queryset.count(),
            "open_jobs": jobs_queryset.filter(status=Job.Status.OPEN).count(),
            "closed_jobs": jobs_queryset.filter(status=Job.Status.CLOSED).count(),
            "total_applications": applications_queryset.count(),
            "pending_applications": applications_queryset.filter(
                status=Application.Status.PENDING
            ).count(),
            "reviewed_applications": applications_queryset.filter(
                status=Application.Status.REVIEWED
            ).count(),
            "accepted_applications": applications_queryset.filter(
                status=Application.Status.ACCEPTED
            ).count(),
            "rejected_applications": applications_queryset.filter(
                status=Application.Status.REJECTED
            ).count(),
        }

        serializer = EmployerDashboardSummarySerializer(summary_data)
        return Response(serializer.data)