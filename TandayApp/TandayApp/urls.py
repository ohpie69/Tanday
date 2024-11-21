"""
URL configuration for TandayApp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from api.views import login_view, register_view, home_view, booking_page, logout_view,hotel_login_view, hotel_registration_view, success, book_now, landing_page_view, my_bookings, edit_booking, delete_booking, hotel_dashboard, add_listing, listings_view, update_listing, delete_listing

urlpatterns = [
    path('', landing_page_view),
    path('admin/', admin.site.urls),
    path('login/', login_view, name='login'),
     path('hotel-dashboard/', hotel_dashboard, name='hotel_dashboard'),
    path('add-listing/', add_listing, name='add_listing'),
    path('register/', register_view, name='register'),
    path('hotel_login/', hotel_login_view, name='hotel_login'),
     path('hotel_register/', hotel_registration_view, name='hotel_register'),
    path('home/', home_view, name='home'),
    path('booking/', booking_page, name='booking'),
    path('logout/', logout_view, name='logout'),
    path('success/', success, name='success'),
    path('book_now', book_now, name= 'book_now'),
    path('my_bookings/', my_bookings, name='my_bookings'),
    path('edit_booking/<int:booking_id>/', edit_booking, name='edit_booking'),
    path('delete_booking/<int:booking_id>/', delete_booking, name='delete_booking'),
    path('listings/', listings_view, name='listings'),
     path('update_listing/<int:listing_id>/', update_listing, name='update_listing'),
    path('delete_listing/<int:listing_id>/', delete_listing, name='delete_listing'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
