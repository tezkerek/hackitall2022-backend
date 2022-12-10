from django.db import models


class Operation(models.Model):
    name = models.CharField(max_length=100)


class Schedule(models.Model):
    start_hour = models.IntegerField()
    start_minute = models.IntegerField()
    end_hour = models.IntegerField()
    end_minute = models.IntegerField()


# Create your models here.
class Branch(models.Model):
    branch_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    operations = models.ManyToManyField(Operation)

    street = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    county = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()

    mf_schedule = models.ForeignKey(
        Schedule, on_delete=models.CASCADE, related_name="mf_schedule"
    )

    is_weekend_open = models.BooleanField()
    is_sunday_open = models.BooleanField()
    satsun_schedule = models.ForeignKey(
        Schedule, on_delete=models.CASCADE, related_name="satsun_schedule"
    )

    has_break = models.BooleanField()
    break_schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name="break_schedule")


class PhoneNumber(models.Model):
    number = models.CharField(max_length=20)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)