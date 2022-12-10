from django.shortcuts import render
from rest_framework import mixins, viewsets

from .models import Branch
from .serializers import BranchSerializer


class BranchViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Branch.objects.prefetch_related(
        "phonenumber_set", "operations"
    ).select_related("mf_schedule", "satsun_schedule", "break_schedule")
    serializer_class = BranchSerializer
