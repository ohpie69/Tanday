from django.contrib import admin
from .models import Listing,Rooms,Filter,Hotel,Booking


admin.site.register(Booking)
admin.site.register(Hotel)
admin.site.register(Listing)
admin.site.register(Filter)
admin.site.register(Rooms)


