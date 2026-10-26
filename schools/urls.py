from django.urls import path
from . import views

app_name = "schools"

urlpatterns = [
    path("register/", views.school_signup, name="school_signup"),
    path(
        "registration-pending/",
        views.school_registration_pending,
        name="school_registration_pending",
    ),
    path("dashboard/", views.dashboard, name="dashboard"),
    path(
        "dashboard/pending/",
        views.dashboard_pending,
        name="dashboard_pending",
    ),
    path(
        "dashboard/rejected/",
        views.dashboard_rejected,
        name="dashboard_rejected",
    ),
    path(
        "dashboard/school/",
        views.school_dashboard,
        name="school_dashboard",
    ),

    path("login/", views.school_login, name="school_login"),

    path(
        "portal/",
        views.school_portal,
        name="school_portal",
    ),

]