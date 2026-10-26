"""
URL configuration for digitalexeat project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from schools import views as school_views
from accounts import views as account_views

urlpatterns = [
    path("", school_views.home, name="home"),
    path("admin/", admin.site.urls),

    # School registration and dashboards
    path("schools/", include("schools.urls")),

    # Django login, logout and password reset routes
    path("accounts/", include("allauth.urls")),
    path("students/", include("students.urls")),
    path(
        "services/",
        account_views.service_selection,
        name="service_selection",
    ),
]
