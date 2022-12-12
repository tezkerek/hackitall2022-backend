from django.db.models import Exists, OuterRef, Q
from django.http import QueryDict
from django.db.models import QuerySet
from rest_framework import mixins, viewsets

from appointments.models import Appointment

from .models import Branch, Operation
from .serializers import BranchSerializer, OperationSerializer


def filter_branches_by_availability(
    queryset: QuerySet, avail_from: str, avail_until: str
):
    overlap_expr = (
        Q(start_date=avail_from, end_date=avail_until)
        | Q(start_date__lt=avail_from, end_date__gt=avail_from)
        | Q(
            start_date__lt=avail_until,
            end_date__gt=avail_until,
        )
    )

    overlapping_appts = Appointment.objects.filter(branch=OuterRef("pk")).filter(
        overlap_expr
    )

    return queryset.filter(~Exists(overlapping_appts))


class BranchViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = BranchSerializer

    def get_queryset(self):
        queryset = Branch.objects.prefetch_related(
            "phonenumber_set", "operations"
        ).select_related("mf_schedule", "satsun_schedule", "break_schedule")

        query_params: QueryDict = self.request.query_params
        avail_from: str | None = query_params.get("available_from")
        avail_until: str | None = query_params.get("available_until")

        if avail_from is not None and avail_until is not None:
            queryset = filter_branches_by_availability(
                queryset, avail_from, avail_until
            )
        return queryset


class OperationViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Operation.objects.all()
    serializer_class = OperationSerializer
