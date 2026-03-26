from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class Application(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        REVIEWED = "reviewed", "Reviewed"
        ACCEPTED = "accepted", "Accepted"
        REJECTED = "rejected", "Rejected"

    applicant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="applications",
    )
    job = models.ForeignKey(
        "jobs.Job",
        on_delete=models.CASCADE,
        related_name="applications",
    )
    cover_letter = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-applied_at"]
        verbose_name = "Application"
        verbose_name_plural = "Applications"
        constraints = [
            models.UniqueConstraint(
                fields=["applicant", "job"],
                name="unique_applicant_job_application",
            )
        ]

    def clean(self) -> None:
        super().clean()

        if self.applicant and self.applicant.role != "applicant":
            raise ValidationError(
                {"applicant": "Only users with applicant role can apply for jobs."}
            )

        if self.job and self.job.status != "open":
            raise ValidationError(
                {"job": "Applications can only be submitted to open jobs."}
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.applicant.username} -> {self.job.title}"