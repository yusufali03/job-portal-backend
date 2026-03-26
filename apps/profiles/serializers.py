from rest_framework import serializers

from .models import ApplicantProfile, EmployerProfile


class ApplicantProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)
    role = serializers.CharField(source="user.role", read_only=True)
    profile_image = serializers.ImageField(required=False, allow_null=True)
    resume_file = serializers.FileField(required=False, allow_null=True)

    class Meta:
        model = ApplicantProfile
        fields = (
            "id",
            "user",
            "username",
            "email",
            "role",
            "full_name",
            "profile_image",
            "phone_number",
            "bio",
            "education",
            "skills",
            "experience",
            "location",
            "portfolio_link",
            "linkedin_link",
            "resume_file",
            "resume_link",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "user",
            "username",
            "email",
            "role",
            "created_at",
            "updated_at",
        )

class EmployerProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)
    role = serializers.CharField(source="user.role", read_only=True)

    class Meta:
        model = EmployerProfile
        fields = (
            "id",
            "user",
            "username",
            "email",
            "role",
            "contact_person_name",
            "company_name",
            "company_description",
            "company_website",
            "phone_number",
            "company_location",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "user",
            "username",
            "email",
            "role",
            "created_at",
            "updated_at",
        )