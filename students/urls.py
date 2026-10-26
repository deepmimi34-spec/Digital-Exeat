from django.urls import path
from . import views

app_name = "students"

urlpatterns = [
    path(
        "link-child/",
        views.link_child,
        name="link_child",
    ),
    path(
        "student-access/",
        views.student_access,
        name="student_access",
    ),
    path(
        "school-directory/",
        views.school_directory,
        name="school_directory",
    ),
]