from django.urls import path

from .views import ApplicantProfileMeView, EmployerProfileMeView

app_name = "profiles"

urlpatterns = [
    path("applicant/me/", ApplicantProfileMeView.as_view(), name="applicant-profile-me"),
    path("employer/me/", EmployerProfileMeView.as_view(), name="employer-profile-me"),
]