from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
import uuid
from django.utils import timezone

# Hotel Manager for custom hotel authentication
class HotelManager(models.Manager):
    def authenticate_hotel(self, username, password):
        try:
            hotel = self.get(username=username)
            if check_password(password, hotel.password):
                return hotel
        except Hotel.DoesNotExist:
            return None


class Listing(models.Model):
    hotel_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    title = models.CharField(max_length=255)
    description = models.TextField()
    price_per_night = models.CharField(max_length=55)
    image = models.ImageField(upload_to='listings/')
    filters = models.ManyToManyField('Filter', related_name="listings")

    def get_average_rating(self):
        reviews = self.reviews_set.all()
        if not reviews:
            return 0
        return round(sum(review.rating for review in reviews) / len(reviews), 1)

    def get_review_count(self):
        return self.reviews_set.count()

class Rooms(models.Model):
    name = models.CharField(max_length=100)
    number_of_beds = models.IntegerField()
    price = models.FloatField()
    listing = models.ForeignKey('Listing', on_delete=models.CASCADE)
    available_room = models.IntegerField(default=1)

    def __str__(self):
        return self.name  

class Booking(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Canceled", "Canceled"),
        ("Accepted", "Accepted"),
        ("Check-in", "Check-in"),
        ("Check-out", "Check-out"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    check_in = models.DateField(null=True, blank=True)
    check_out = models.DateField(null=True, blank=True)
    guests = models.IntegerField()
    room = models.ForeignKey(Rooms, on_delete=models.CASCADE)
    booking_number = models.CharField(max_length=12, editable=False, default=timezone.now().strftime('%Y%m%d%H%M%S') + uuid.uuid4().hex[:14].upper())
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Pending")
    isReviewed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.booking_number} - {self.name} ({self.check_in} to {self.check_out})"


class Hotel(models.Model):
    hotel_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    hotel_description = models.TextField()
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255) 

    objects = HotelManager() 

    def save(self, *args, **kwargs):
        if not self.pk: 
            self.password = make_password(self.password) 
        super().save(*args, **kwargs)

    def __str__(self):
        return self.hotel_name

class Filter(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name  


class Reviews(models.Model):
    message = models.TextField()
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timePosted = models.DateField(auto_now_add=True)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], default=5)  # 1-5 star rating

    def __str__(self) -> str:
        return self.message
