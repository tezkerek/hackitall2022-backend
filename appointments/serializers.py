from typing import Dict
from django.http import Http404
from rest_framework import serializers
from branches.models import Branch, Operation
from .models import Appointment


class AppointmentSerializer(serializers.ModelSerializer):
    operations = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Operation.objects.all()
    )
    branch_id = serializers.PrimaryKeyRelatedField(queryset=Branch.objects.all())

    class Meta:
        model = Appointment
        fields = (
            "operations",
            "branch_id",
            "start_date",
            "end_date",
            "first_name",
            "last_name",
            "cnp",
            "email",
            "phone_number",
            "comment",
        )

    def create(self, validated_data: Dict):
        operations = validated_data.pop("operations")

        print(Appointment(**validated_data))
        appointment = Appointment.objects.create(**validated_data)

        for op in operations:
            appointment.operations.add(op)

        return appointment
