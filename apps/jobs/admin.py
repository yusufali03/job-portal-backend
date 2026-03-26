from django.contrib import admin

from .models import Job


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "employer",
        "category",
        "location",
        "job_type",
        "status",
        "application_deadline",
        "created_at",
    )
    list_filter = (
        "status",
        "job_type",
        "category",
        "location",
    )
    search_fields = (
        "title",
        "category",
        "location",
        "employer__username",
        "employer__email",
    )
    ordering = ("-created_at",)
    list_select_related = ("employer",)
