from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
import uuid

# Hotel Manager for custom hotel authentication
class HotelManager(models.Manager):
    def authenticate_hotel(self, username, password):
        try:
            hotel = self.get(username=username)
            if check_password(password, hotel.password):  # Use check_password to verify the hashed password
                return hotel
        except Hotel.DoesNotExist:
            return None

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    hotel = models.ForeignKey('Hotel', on_delete=models.CASCADE, null=True, blank=True)  # Link to hotel
    name = models.CharField(max_length=100)
    email = models.EmailField()
    check_in = models.DateField(null=True, blank=True)
    check_out = models.DateField(null=True, blank=True)
    guests = models.IntegerField()
    room_types = models.TextField(null=True)
    booking_number = models.CharField(max_length=12, editable=False, default=uuid.uuid4().hex[:12].upper())

    def __str__(self):
        return f"{self.booking_number} - {self.name} ({self.check_in} to {self.check_out})"


class Hotel(models.Model):
    hotel_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    hotel_description = models.TextField()
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)  # Store hashed password

    objects = HotelManager()  # Attach the custom manager to the Hotel model

    def save(self, *args, **kwargs):
        if not self.pk:  # Only hash password when the hotel is being created
            self.password = make_password(self.password)  # Hash the password
        super().save(*args, **kwargs)

    def __str__(self):
        return self.hotel_name
    
class Listing(models.Model):
    hotel_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    title = models.CharField(max_length=255)
    description = models.TextField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='listings/')
    filters = models.ManyToManyField('Filter', related_name="listings")
    
    def __str__(self):
        return self.title

class Filter(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name
