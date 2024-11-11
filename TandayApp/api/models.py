from django.db import models
from django.contrib.auth.models import User
import uuid

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    check_in = models.DateField(null=True, blank=True)
    check_out = models.DateField(null=True, blank=True)
    guests = models.IntegerField()
    room_types = models.TextField(null=True)
    booking_number = models.CharField(max_length=12, editable=False, default=uuid.uuid4().hex[:12].upper())

    def __str__(self):
        return f"{self.booking_number} - {self.name} ({self.check_in} to {self.check_out})"
