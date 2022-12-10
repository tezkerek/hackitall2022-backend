from django.shortcuts import render
from rest_framework import mixins, viewsets

from .models import Branch, Operation
from .serializers import BranchSerializer, OperationSerializer


class BranchViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Branch.objects.prefetch_related(
        "phonenumber_set", "operations"
    ).select_related("mf_schedule", "satsun_schedule", "break_schedule")
    serializer_class = BranchSerializer

class OperationViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Operation.objects.all()
    serializer_class = OperationSerializer
