from django.db import models



from django.db import models

class Booking(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    check_in = models.DateField()
    check_out = models.DateField()
    guests = models.IntegerField()
    room_types = models.TextField(null=True)  # Allow null values


    def __str__(self):
        return f"{self.name} - {self.check_in} to {self.check_out}"
# Create your models here.
