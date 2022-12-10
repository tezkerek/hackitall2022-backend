from typing import Dict
from django.http import Http404
from rest_framework import serializers
from branches.models import Branch, Operation
from .models import Appointment


class AppointmentSerializer(serializers.ModelSerializer):
    operations = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Operation.objects.all()
    )
    branch_id = serializers.IntegerField(source="branch.branch_id")

    class Meta:
        model = Appointment
        fields = (
            "operations",
            "branch_id",
            "date",
            "duration",
            "first_name",
            "last_name",
            "cnp",
            "email",
            "phone_number",
            "comment",
        )

    def create(self, validated_data: Dict):
        print(validated_data)
        branch_id = validated_data.pop("branch")["branch_id"]
        try:
            branch = Branch.objects.filter(branch_id=branch_id).first()
        except:
            raise Http404

        operations = validated_data.pop("operations")

        print(Appointment(**validated_data))
        appointment = Appointment.objects.create(
            **validated_data,
            branch=branch,
        )

        for op in operations:
            appointment.operations.add(op)

        return appointment
