from django.db import models
from branches.models import Branch, Operation


class Appointment(models.Model):
    operations = models.ManyToManyField(Operation)

    branch = models.ForeignKey(Branch, on_delete=models.RESTRICT)
    date = models.DateTimeField()
    duration = models.IntegerField()

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    cnp = models.CharField(max_length=30)
    email = models.EmailField(max_length=100)
    phone_number = models.CharField(max_length=20)
    comment = models.CharField(max_length=255, blank=True)
