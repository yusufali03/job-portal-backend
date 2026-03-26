from django.contrib import admin

from .models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "applicant",
        "job",
        "status",
        "applied_at",
    )
    list_filter = (
        "status",
        "applied_at",
    )
    search_fields = (
        "applicant__username",
        "applicant__email",
        "job__title",
    )
    ordering = ("-applied_at",)
    list_select_related = ("applicant", "job")
