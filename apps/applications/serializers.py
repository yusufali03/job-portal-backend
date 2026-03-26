from rest_framework import serializers

from .models import Application


class ApplicationSerializer(serializers.ModelSerializer):
    applicant_username = serializers.CharField(source="applicant.username", read_only=True)
    job_title = serializers.CharField(source="job.title", read_only=True)
    job_location = serializers.CharField(source="job.location", read_only=True)
    job_type = serializers.CharField(source="job.job_type", read_only=True)
    employer_company_name = serializers.SerializerMethodField()

    class Meta:
        model = Application
        fields = (
            "id",
            "applicant",
            "applicant_username",
            "job",
            "job_title",
            "job_location",
            "job_type",
            "employer_company_name",
            "cover_letter",
            "status",
            "applied_at",
        )
        read_only_fields = ("id", "applicant", "status", "applied_at")

    def get_employer_company_name(self, obj):
        employer_profile = getattr(obj.job.employer, "employer_profile", None)
        return employer_profile.company_name if employer_profile else obj.job.employer.username


class ApplicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ("id", "job", "cover_letter")
        read_only_fields = ("id",)

    def create(self, validated_data):
        validated_data["applicant"] = self.context["request"].user
        return super().create(validated_data)


class EmployerApplicationSerializer(serializers.ModelSerializer):
    applicant_username = serializers.CharField(source="applicant.username", read_only=True)
    applicant_email = serializers.CharField(source="applicant.email", read_only=True)
    job_title = serializers.CharField(source="job.title", read_only=True)

    class Meta:
        model = Application
        fields = (
            "id",
            "applicant",
            "applicant_username",
            "applicant_email",
            "job",
            "job_title",
            "cover_letter",
            "status",
            "applied_at",
        )


class ApplicationStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ("status",)




class ApplicationDetailSerializer(serializers.ModelSerializer):
    job_title = serializers.CharField(source="job.title", read_only=True)
    applicant_id = serializers.IntegerField(source="applicant.id", read_only=True)
    applicant_username = serializers.CharField(source="applicant.username", read_only=True)
    applicant_email = serializers.CharField(source="applicant.email", read_only=True)
    applicant_full_name = serializers.CharField(
        source="applicant.applicant_profile.full_name",
        read_only=True,
        default="",
    )
    applicant_phone_number = serializers.CharField(
        source="applicant.applicant_profile.phone_number",
        read_only=True,
        default="",
    )
    applicant_education = serializers.CharField(
        source="applicant.applicant_profile.education",
        read_only=True,
        default="",
    )
    applicant_skills = serializers.CharField(
        source="applicant.applicant_profile.skills",
        read_only=True,
        default="",
    )
    applicant_experience = serializers.CharField(
        source="applicant.applicant_profile.experience",
        read_only=True,
        default="",
    )
    applicant_resume_link = serializers.CharField(
        source="applicant.applicant_profile.resume_link",
        read_only=True,
        default="",
    )

    class Meta:
        model = Application
        fields = (
            "id",
            "status",
            "applied_at",
            "cover_letter",
            "job",
            "job_title",
            "applicant_id",
            "applicant_username",
            "applicant_email",
            "applicant_full_name",
            "applicant_phone_number",
            "applicant_education",
            "applicant_skills",
            "applicant_experience",
            "applicant_resume_link",
        )

class MyApplicationDetailSerializer(serializers.ModelSerializer):
    job_title = serializers.CharField(source="job.title", read_only=True)
    job_description = serializers.CharField(source="job.description", read_only=True)
    job_requirements = serializers.CharField(source="job.requirements", read_only=True)
    job_location = serializers.CharField(source="job.location", read_only=True)
    job_type = serializers.CharField(source="job.job_type", read_only=True)
    employer_company_name = serializers.SerializerMethodField()

    class Meta:
        model = Application
        fields = (
            "id",
            "status",
            "applied_at",
            "cover_letter",
            "job",
            "job_title",
            "job_description",
            "job_requirements",
            "job_location",
            "job_type",
            "employer_company_name",
        )

    def get_employer_company_name(self, obj):
        employer_profile = getattr(obj.job.employer, "employer_profile", None)
        return employer_profile.company_name if employer_profile else obj.job.employer.username