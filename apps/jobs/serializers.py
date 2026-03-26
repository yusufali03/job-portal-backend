from rest_framework import serializers

from .models import Job


class JobListSerializer(serializers.ModelSerializer):
    employer_username = serializers.CharField(source="employer.username", read_only=True)

    class Meta:
        model = Job
        fields = (
            "id",
            "title",
            "category",
            "location",
            "job_type",
            "status",
            "salary",
            "application_deadline",
            "employer_username",
            "created_at",
        )


class JobDetailSerializer(serializers.ModelSerializer):
    employer_username = serializers.CharField(source="employer.username", read_only=True)

    class Meta:
        model = Job
        fields = (
            "id",
            "title",
            "category",
            "location",
            "description",
            "requirements",
            "salary",
            "job_type",
            "status",
            "application_deadline",
            "employer",
            "employer_username",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "employer", "created_at", "updated_at")


class JobCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = (
            "id",
            "title",
            "category",
            "location",
            "description",
            "requirements",
            "salary",
            "job_type",
            "status",
            "application_deadline",
        )
        read_only_fields = ("id",)

    def create(self, validated_data):
        validated_data["employer"] = self.context["request"].user
        return super().create(validated_data)


class EmployerDashboardSummarySerializer(serializers.Serializer):
    total_jobs = serializers.IntegerField()
    open_jobs = serializers.IntegerField()
    closed_jobs = serializers.IntegerField()
    total_applications = serializers.IntegerField()
    pending_applications = serializers.IntegerField()
    reviewed_applications = serializers.IntegerField()
    accepted_applications = serializers.IntegerField()
    rejected_applications = serializers.IntegerField()