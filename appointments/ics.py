from icalendar import Calendar, Event, vText
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db.models import ObjectDoesNotExist

from .models import Appointment


def generate_ics(appointment: Appointment):
    cal = Calendar()
    cal.add("attendee", f"MAILTO:{appointment.email}")

    event = Event()

    try:
        summary = appointment.operations.first()
    except ObjectDoesNotExist:
        summary = appointment.branch.name
    event.add("summary", summary)

    event.add("dtstart", appointment.start_date)
    event.add("dtend", appointment.end_date)
    event["location"] = vText(appointment.branch.street)

    cal.add_component(event)

    path = default_storage.save(
        f"appointment_ics/{appointment.uuid}.ics", ContentFile(cal.to_ical())
    )

    return path
