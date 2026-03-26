from django.contrib import admin

from .models import ApplicantProfile, EmployerProfile


@admin.register(ApplicantProfile)
class ApplicantProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "full_name", "phone_number", "created_at")
    search_fields = ("user__username", "user__email", "full_name", "phone_number")
    ordering = ("id",)
    list_select_related = ("user",)


@admin.register(EmployerProfile)
class EmployerProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user","contact_person_name", "company_name", "company_location", "created_at")
    search_fields = (
        "user__username",
        "user__email",
        "contact_person_name",
        "company_name",
        "company_location",
    )
    ordering = ("id",)
    list_select_related = ("user",)