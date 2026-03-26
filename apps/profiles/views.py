from rest_framework import generics, permissions
from rest_framework.exceptions import NotFound
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser

from .models import ApplicantProfile, EmployerProfile
from .serializers import ApplicantProfileSerializer, EmployerProfileSerializer


class ApplicantProfileMeView(generics.RetrieveUpdateAPIView):
    serializer_class = ApplicantProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def get_object(self):
        user = self.request.user

        if user.role != "applicant":
            raise NotFound("Applicant profile not found.")

        profile, _ = ApplicantProfile.objects.get_or_create(
            user=user,
            defaults={
                "full_name": user.username,
            },
        )
        return profile


class EmployerProfileMeView(generics.RetrieveUpdateAPIView):
    serializer_class = EmployerProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_object(self):
        user = self.request.user

        if user.role != "employer":
            raise NotFound("Employer profile not found.")

        profile, _ = EmployerProfile.objects.get_or_create(
            user=user,
            defaults={
                "company_name": "",
            },
        )
        return profile