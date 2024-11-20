from django.contrib import admin
from .models import Booking
from .models import Hotel
from .models import Listing
from .models import Filter

admin.site.register(Booking)
admin.site.register(Hotel)
admin.site.register(Listing)
admin.site.register(Filter)


