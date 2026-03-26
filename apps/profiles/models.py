from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
import os

def validate_resume_file(value) -> None:
    allowed_extensions = [".pdf"]
    ext = os.path.splitext(value.name)[1].lower()

    if ext not in allowed_extensions:
        raise ValidationError("Only PDF files are allowed for resume upload.")


def validate_profile_image(value) -> None:
    allowed_extensions = [".jpg", ".jpeg", ".png", ".webp"]
    ext = os.path.splitext(value.name)[1].lower()

    if ext not in allowed_extensions:
        raise ValidationError("Only JPG, JPEG, PNG, and WEBP images are allowed.")


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BaseProfile(TimeStampedModel):
    REQUIRED_ROLE = None

    class Meta:
        abstract = True

    def clean(self) -> None:
        super().clean()
        user = getattr(self, "user", None)

        if self.REQUIRED_ROLE and user and user.role != self.REQUIRED_ROLE:
            raise ValidationError(
                {
                    "user": (
                        f"This profile can only be linked to a user with "
                        f"'{self.REQUIRED_ROLE}' role."
                    )
                }
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class ApplicantProfile(BaseProfile):
    REQUIRED_ROLE = "applicant"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="applicant_profile",
    )
    full_name = models.CharField(max_length=150)
    profile_image = models.ImageField(upload_to="profile_images/applicants/", blank=True, null=True, validators=[validate_profile_image])
    phone_number = models.CharField(max_length=20, blank=True)
    bio = models.TextField(blank=True)
    education = models.CharField(max_length=255, blank=True)
    skills = models.TextField(blank=True)
    experience = models.TextField(blank=True)
    location = models.CharField(max_length=150, blank=True)
    portfolio_link = models.URLField(blank=True)
    linkedin_link = models.URLField(blank=True)
    resume_file = models.FileField(upload_to="resumes/", blank=True, null=True, validators=[validate_resume_file])
    resume_link = models.URLField(blank=True)

    class Meta:
        verbose_name = "Applicant Profile"
        verbose_name_plural = "Applicant Profiles"

    def __str__(self) -> str:
        return f"{self.full_name} - Applicant"

class EmployerProfile(BaseProfile):
    REQUIRED_ROLE = "employer"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="employer_profile",
    )
    contact_person_name = models.CharField(max_length=150, blank=True)
    company_name = models.CharField(max_length=150, blank=True)
    company_description = models.TextField(blank=True)
    company_website = models.URLField(blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    company_location = models.CharField(max_length=150, blank=True)

    class Meta:
        verbose_name = "Employer Profile"
        verbose_name_plural = "Employer Profiles"

    def __str__(self) -> str:
        return self.company_name


