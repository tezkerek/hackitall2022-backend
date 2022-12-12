"""bcr URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import routers
from branches.views import BranchViewSet, OperationViewSet
from appointments.views import (
    AppointmentViewSet,
    email_view,
    delete_appointment,
    download_appointment_ics,
)

router = routers.SimpleRouter()
router.register(r"operations", OperationViewSet, basename="branch")
router.register(r"branches", BranchViewSet, basename="branch")
router.register(r"appointments", AppointmentViewSet, basename="appointment")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(router.urls)),
    path("email/", email_view),
    path("delete-appointment/<uuid>", delete_appointment),
    path("appointment-ics/<uuid>", download_appointment_ics),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
