from rest_framework import serializers
from .models import Branch, Operation, PhoneNumber, Schedule


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ("start_hour", "start_minute", "end_hour", "end_minute")


class BranchSerializer(serializers.ModelSerializer):
    phone_numbers = serializers.StringRelatedField(many=True, source="phonenumber_set")
    operations = serializers.StringRelatedField(many=True)
    mf_schedule = ScheduleSerializer(read_only=True)
    satsun_schedule = ScheduleSerializer(read_only=True)
    break_schedule = ScheduleSerializer(read_only=True)

    class Meta:
        model = Branch
        fields = (
            "branch_id",
            "name",
            "operations",
            "street",
            "city",
            "county",
            "latitude",
            "longitude",
            "phone_numbers",
            "mf_schedule",
            "is_weekend_open",
            "is_sunday_open",
            "satsun_schedule",
            "has_break",
            "break_schedule",
        )
