from django.urls import path

from .views import JobListCreateView, JobRetrieveUpdateDestroyView, EmployerJobListView, EmployerDashboardSummaryView

app_name = "jobs"

urlpatterns = [
    path("", JobListCreateView.as_view(), name="job-list-create"),
    path("my/", EmployerJobListView.as_view(), name="my-jobs"),
    path("dashboard/summary/", EmployerDashboardSummaryView.as_view(), name="employer-dashboard-summary"),
    path("<int:pk>/", JobRetrieveUpdateDestroyView.as_view(), name="job-detail"),
]