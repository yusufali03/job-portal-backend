from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        APPLICANT = "applicant", "Applicant"
        EMPLOYER = "employer", "Employer"
        ADMIN = "admin", "Admin"

    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.APPLICANT,
    )

    def __str__(self) -> str:
        return f"{self.username} ({self.role})"
