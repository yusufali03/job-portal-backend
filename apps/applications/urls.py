from django.urls import path

from .views import (
    ApplicationCreateView,
    EmployerJobApplicationListView,
    MyApplicationListView, ApplicationStatusUpdateView, ApplicationDetailView, MyApplicationDetailView,
)

app_name = "applications"

urlpatterns = [
    path("", ApplicationCreateView.as_view(), name="application-create"),
    path("my/", MyApplicationListView.as_view(), name="my-applications"),
    path("<int:pk>/my-detail/", MyApplicationDetailView.as_view(), name="my-application-detail"),
    path("<int:pk>/detail/", ApplicationDetailView.as_view(), name="application-detail"),
    path("job/<int:job_id>/", EmployerJobApplicationListView.as_view(), name="job-applications"),
    path("<int:pk>/status/", ApplicationStatusUpdateView.as_view(), name="application-status-update")
]