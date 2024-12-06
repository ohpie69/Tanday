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
from api.views import review, login_view,add_room_view,booking_details ,viewBooks,acceptBooking, register_view,filter_hotel_view, home_view, booking_page, logout_view,hotel_login_view, hotel_registration_view, success, book_now, landing_page_view, my_bookings, edit_booking, delete_booking, hotel_dashboard, add_listing, listings_view, update_listing, delete_listing, edit_user

urlpatterns = [
    path('', landing_page_view, name='landing'),
    path('admin/', admin.site.urls),
    path('login/', login_view, name='login'),
    path('hotel-dashboard/', hotel_dashboard, name='hotel_dashboard'),
    path('add-listing/', add_listing, name='add_listing'),
    path('add-room/<int:listing_id>/', add_room_view, name='add_room'),
    
    path('viewBooks/<int:listing_id>/', viewBooks, name='viewBooks'),
    path('accept/<int:booking_id>/', acceptBooking, name='accept'),

    path('review/<int:booking_id>/', review, name = 'review'),

    path('register/', register_view, name='register'),
    path('hotel_login/', hotel_login_view, name='hotel_login'),
    path('hotel_register/', hotel_registration_view, name='hotel_register'),
    path('home/', home_view, name='home'),
    path('booking/<int:listing_id>/', booking_page, name='booking'),
    path('logout/', logout_view, name='logout'),
    path('success/', success, name='success'),
    path('booking_details/<int:booking_id>', booking_details, name='booking_details'),
    path('book_now/', book_now, name= 'book_now'),
    path('my_bookings/', my_bookings, name='my_bookings'),
    path('edit_booking/<int:booking_id>/', edit_booking, name='edit_booking'),
    path('delete_booking/<int:booking_id>/', delete_booking, name='delete_booking'),
    path('listings/', listings_view, name='listings'),

    path('filter_hotel/<str:filter_value>', filter_hotel_view, name='filter_hotel'),
    
    path('update_listing/<int:listing_id>/', update_listing, name='update_listing'),
    path('delete_listing/<int:listing_id>/', delete_listing, name='delete_listing'),
    path('edit_user/', edit_user, name='edit_user'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
