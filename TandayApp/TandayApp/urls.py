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
from django.contrib import admin
from django.urls import path
from api.views import login_view, register_view, home_view, booking_page, logout_view,hotel_login_view, hotel_registration_view, success, book_now # Ensure logout_view is imported

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('hotel_login/', hotel_login_view, name='hotel_login'),
     path('hotel_register/', hotel_registration_view, name='hotel_register'),
    path('home/', home_view, name='home'),
    path('booking/', booking_page, name='booking'),
    path('logout/', logout_view, name='logout'),  # Ensure this line is present
    path('success/', success, name='success'),
    path('book_now', book_now, name= 'book_now')
]
