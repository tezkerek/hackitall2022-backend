from typing import Dict
from rest_framework import serializers
from branches.models import Branch, Operation
from .models import Appointment
from .ics import generate_ics


class AppointmentSerializer(serializers.ModelSerializer):
    operations = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Operation.objects.all()
    )

    class Meta:
        model = Appointment
        fields = (
            "operations",
            "branch",
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

        appointment = Appointment.objects.create(**validated_data)

        for op in operations:
            appointment.operations.add(op)

        ics_path = generate_ics(appointment)

        return appointment
