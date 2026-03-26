from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class Job(models.Model):
    class JobType(models.TextChoices):
        FULL_TIME = "full_time", "Full Time"
        PART_TIME = "part_time", "Part Time"
        INTERNSHIP = "internship", "Internship"
        REMOTE = "remote", "Remote"

    class Status(models.TextChoices):
        OPEN = "open", "Open"
        CLOSED = "closed", "Closed"

    employer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="jobs",
    )
    title = models.CharField(max_length=150)
    category = models.CharField(max_length=100)
    location = models.CharField(max_length=150)
    description = models.TextField()
    requirements = models.TextField()
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    job_type = models.CharField(
        max_length=20,
        choices=JobType.choices,
        default=JobType.FULL_TIME,
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.OPEN,
    )
    application_deadline = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Job"
        verbose_name_plural = "Jobs"

    def clean(self) -> None:
        super().clean()

        if self.employer and self.employer.role != "employer":
            raise ValidationError(
                {"employer": "Only users with employer role can create jobs."}
            )

        if self.salary is not None and self.salary < 0:
            raise ValidationError(
                {"salary": "Salary cannot be negative."}
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.title} - {self.employer.username}"