from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied, NotFound

from apps.jobs.models import Job
from apps.users.permissions import IsApplicantRole, IsEmployerRole


from .models import Application
from .serializers import (
    ApplicationCreateSerializer,
    ApplicationDetailSerializer,
    ApplicationSerializer,
    ApplicationStatusUpdateSerializer,
    EmployerApplicationSerializer, MyApplicationDetailSerializer,
)


class ApplicationCreateView(generics.CreateAPIView):
    serializer_class = ApplicationCreateSerializer
    permission_classes = [permissions.IsAuthenticated, IsApplicantRole]

    def perform_create(self, serializer):
        serializer.save(applicant=self.request.user)


class MyApplicationListView(generics.ListAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated, IsApplicantRole]

    def get_queryset(self):
        return Application.objects.select_related(
            "applicant",
            "job",
            "job__employer",
            "job__employer__employer_profile",
        ).filter(applicant=self.request.user)

class MyApplicationDetailView(generics.RetrieveAPIView):
    serializer_class = MyApplicationDetailSerializer
    permission_classes = [permissions.IsAuthenticated, IsApplicantRole]
    queryset = Application.objects.select_related(
        "job",
        "job__employer",
        "job__employer__employer_profile",
        "applicant",
    )

    def get_object(self):
        application = super().get_object()

        if application.applicant != self.request.user:
            raise PermissionDenied(
                "You do not have permission to view this application."
            )

        return application

class EmployerJobApplicationListView(generics.ListAPIView):
    serializer_class = EmployerApplicationSerializer
    permission_classes = [permissions.IsAuthenticated, IsEmployerRole]

    def get_queryset(self):
        job_id = self.kwargs["job_id"]

        try:
            job = Job.objects.get(id=job_id, employer=self.request.user)
        except Job.DoesNotExist as exc:
            raise PermissionDenied(
                "You do not have permission to view applications for this job."
            ) from exc

        return Application.objects.select_related("applicant", "job").filter(job=job)


class ApplicationStatusUpdateView(generics.UpdateAPIView):
    serializer_class = ApplicationStatusUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, IsEmployerRole]
    queryset = Application.objects.select_related("job", "applicant")

    def get_object(self):
        application = super().get_object()

        if application.job.employer != self.request.user:
            raise PermissionDenied(
                "You do not have permission to update this application."
            )

        return application

class ApplicationDetailView(generics.RetrieveAPIView):
    serializer_class = ApplicationDetailSerializer
    permission_classes = [permissions.IsAuthenticated, IsEmployerRole]
    queryset = Application.objects.select_related(
        "job",
        "applicant",
        "applicant__applicant_profile",
    )

    def get_object(self):
        application = super().get_object()

        if application.job.employer != self.request.user:
            raise PermissionDenied(
                "You do not have permission to view this application."
            )

        return application