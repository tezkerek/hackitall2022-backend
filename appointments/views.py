from django.conf import settings
from django.shortcuts import render
from django.http import Http404, HttpResponse
from django.views.decorators.http import require_http_methods
from django.core.files.storage import default_storage
from rest_framework import mixins, viewsets
from .models import Appointment
from .serializers import AppointmentSerializer


class AppointmentViewSet(
    mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet
):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer


@require_http_methods(["GET"])
def delete_appointment(request, uuid):
    deleted_count = Appointment.objects.filter(uuid=uuid).delete()
    if deleted_count == 0:
        raise Http404
    return render(request, "delete_appointment.html")


@require_http_methods(["GET"])
def download_appointment_ics(request, uuid):
    path = f"appointment_ics/{uuid}.ics"
    if not default_storage.exists(path):
        raise Http404

    response = HttpResponse(
        default_storage.open(path).read(),
        headers={
            "Content-Type": "text/calendar",
            "Content-Disposition": "attachment; filename=bcr.ics",
        },
    )
    return response


@require_http_methods(["GET"])
def email_view(request):
    appt: Appointment = Appointment.objects.select_related("branch").first()
    context = {
        "first_name": appt.first_name,
        "branch_name": appt.branch.name,
        "operation_name": appt.operations.first().name,
        "date": appt.start_date.strftime("%-d %b %Y"),
        "start_time": appt.start_date.strftime("%-H:%M"),
        "end_time": appt.end_date.strftime("%-H:%M"),
        "street": appt.branch.street,
        "map_preview_url": (
            f"https://maps.googleapis.com/maps/api/staticmap"
            f"?center={appt.branch.latitude},{appt.branch.longitude}"
            f"&markers=color:0x409ae2|{appt.branch.latitude},{appt.branch.longitude}"
            f"&zoom=16&size=500x300&maptype=normal"
            f"&key={settings.MAPS_API_KEY}"
        ),
        "map_directions_url": (
            f"https://www.google.com/maps/dir/?api=1"
            f"&destination={appt.branch.latitude},{appt.branch.longitude}"
        ),
        "appointment_ics_url": f"/appointment-ics/{appt.uuid}",
        "delete_appointment_url": f"/delete-appointment/{appt.uuid}",
    }
    return render(request, "email.html", context)
