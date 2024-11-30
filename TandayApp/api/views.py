from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UserUpdateForm,RoomForm, BookingForm,EditBookingForm, HotelRegistrationForm, HotelLoginForm, ListingForm
from django.contrib import messages
from .models import Booking, Hotel, Listing, Filter, Rooms
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.hashers import check_password
import logging
from django.db import models
from django.utils import timezone


# Set up logging
logger = logging.getLogger(__name__)

# Create your views here.

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error_message = "Incorrect username or password. Please try again." 
            return render(request, 'login.html', {'error': error_message})
    return render(request, 'login.html')



def hotel_login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_staff:
                login(request, user)
                return redirect('hotel_dashboard')
            else:
                return redirect('login')
            
        else:
            error_message = "Incorrect username or password. Please try again." 
            return render(request, 'hotel_login.html', {'error': error_message})
    return render(request, 'hotel_login.html')


@login_required
def home_view(request):
    search_query = request.GET.get('search', '')
    listings = Listing.objects.all()  
    filters = Filter.objects.all()

    filter_query = request.GET.get('filter', '')

    if search_query:
        listings = listings.filter(
            title__icontains=search_query
        ) | listings.filter(
            description__icontains=search_query
        )

    if filter_query:
        listings = listings.filter(filters__name=filter_query)  


    context = {
        'listings': listings,
        'search_query': search_query,
        'filters': filters,
    }
    return render(request, 'home.html', context)

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save() 
                login(request, user) 
                return redirect('home') 
            except Exception as e:
                print(f"Error saving user: {e}")
        else:
            print(form.errors)  
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})


def hotel_registration_view(request):
    if request.method == 'POST':
        form = HotelRegistrationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()  
                login(request, user)  
                return redirect('hotel_dashboard')  
            except Exception as e:
                form.add_error(None, f"An unexpected error occurred: {e}")  
    else:
        form = HotelRegistrationForm()

    return render(request, 'hotel_register.html', {'form': form})


@login_required
def update_profile_view(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'update_profile.html', {'form': form})

@login_required
def booking_page(request,listing_id):
    current_datetime = timezone.now()
    rooms = Rooms.objects.filter(listing = listing_id)
    for room in rooms:
        print(room.name)

    listing = Listing.objects.all()
    return render(request, 'booking.html', {
        'username': request.user.username,
        'email': request.user.email,  
        'listing':listing,
        'rooms':rooms,
        "current_datetime":current_datetime,
    })

@login_required
def logout_view(request):
    logout(request)
    return redirect('landing')

@login_required
def book_now(request):
   
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        check_in = request.POST.get('check-in')
        check_out = request.POST.get('check-out')
        guests = request.POST.get('guests')
        room_id = request.POST.get('room_id') 
        print("you book: ",room_id)
        room = get_object_or_404(Rooms, pk=room_id)

        error_message = None

        if check_out <= check_in:
            error_message = "Check-out date must be after check-in date."

        if error_message:
            return render(request, 'booking.html', {
                'error': error_message,
                'username': request.user.username,
                'email': email, 
                'name': name,
                'check_in': check_in, 
                'check_out': check_out,
                'guests': guests, 
                
            })

        booking = Booking(
            user=request.user,
            name=name,
            email=email,
            check_in=check_in,
            check_out=check_out,
            guests=guests,
            room=room,
        )
        booking.save() 

        return redirect('success')
    else:
        return render(request, 'booking.html')

@login_required    
def success(request):
    # Get the latest booking for the current user
    booking = Booking.objects.filter(user=request.user).latest('id')
    
    # Pass the booking details to the template
    return render(request, 'success.html', {'booking': booking})

def booking_details(request,booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Pass the booking details to the template
    return render(request, 'success.html', {'booking': booking})

def landing_page_view(request):
    return render(request, 'landingpage.html')

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'my_bookings.html', {'bookings': bookings})

@login_required
def edit_booking(request, booking_id):
    # Retrieve the booking based on the ID
    booking = get_object_or_404(Booking, id=booking_id)
    rooms = Rooms.objects.filter(listing = booking.room.listing)
    
    
    if request.method == 'POST':
        form = EditBookingForm(request.POST, instance=booking)
        getroom = request.POST.get('room') 
        print('The room id is: ',getroom)
        theRoom = get_object_or_404(Rooms, id=getroom)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.room = theRoom
            booking.save()
            messages.success(request, 'Your booking has been updated successfully!')
            return redirect('my_bookings')  # Redirect to the bookings list page
    else:
        # Pre-fill room_types as a list for the form
        
        form = EditBookingForm(instance=booking)

    return render(request, 'edit_booking.html', {
        'form': form,
        'booking': booking,
        "rooms":rooms,
        
    })

@login_required
def delete_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if request.method == 'POST':
        booking.delete()
        return JsonResponse({'success': True}) 

    return JsonResponse({'success': False}, status=400)

@login_required
def hotel_dashboard(request):
    # Get the listings for the logged-in hotel owner
    listings = Listing.objects.filter(hotel_owner = request.user)
    if request.user.is_staff:
        return render(request, 'hotel_dashboard.html', {'listings': listings})

@login_required
def add_listing(request):
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.hotel_owner = request.user
            listing.save()
            form.save_m2m()
            return redirect('add_room',listing_id = listing.id)
    else:
        form = ListingForm()

    return render(request, 'add_listing.html', {'form': form})
@login_required
def add_room_view(request,listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.listing = listing
            room.save()
            return redirect('hotel_dashboard')
    else:
        form = RoomForm()

    return render(request, 'add_rooms.html', {'form': form})
@login_required
def viewBooks(request,listing_id):
    bookings = Booking.objects.filter(room__listing__id=listing_id)
    
    context = {'bookings':bookings,
               }
    return render(request, 'viewHotelBooks.html',context )
@login_required
def acceptBooking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if request.method == 'POST' and 'accept_button' in request.POST:  
        booking.status = 'Accepted'  
        booking.save()  
        messages.success(request, 'The booking has been accepted successfully!')
        print('booking',booking.room.listing.id)
        return redirect('viewBooks',listing_id =booking.room.listing.id)  
    if request.method == 'POST' and 'cancel_button' in request.POST:  
        booking.status = 'Canceled'  
        booking.save()  
        messages.success(request, 'The booking has been accepted successfully!')
        print('successfully')
        return redirect('viewBooks',listing_id =booking.room.listing.id)  
    if request.method == 'POST' and 'check_in_button' in request.POST:  
        booking.status = 'Check-in'  
        booking.save()  
        messages.success(request, 'The booking has been accepted successfully!')
        print('successfully')
        return redirect('viewBooks',listing_id =booking.room.listing.id)  
    
    if request.method == 'POST' and 'Check-In_button' in request.POST:  
        booking.status = 'Check-in'  
        booking.save()  
        messages.success(request, 'The booking has been accepted successfully!')
        print('successfully')
        return redirect('my_bookings')  
    if request.method == 'POST' and 'cancel-user_button' in request.POST:  
        booking.status = 'Canceled'  
        booking.save()  
        messages.success(request, 'The booking has been accepted successfully!')
        print('successfully')
        return redirect('my_bookings') 
    if request.method == 'POST' and 'check-out-user_button' in request.POST:  
        booking.status = 'Check-out'  
        booking.save()  
        messages.success(request, 'The booking has been accepted successfully!')
        print('successfully')
        return redirect('my_bookings') 

    return render(request, 'viewHotelBooks.html', {'booking': booking})

@login_required
def listings_view(request):
    filter_value = request.GET.get('filter', '')
    print("The filter value is:",filter_value)
    if filter_value:
        listings = Listing.objects.filter(filters__name=filter_value)  # Assuming you have a ManyToMany relationship
    else:
        listings = Listing.objects.all()
   
    return render(request, 'home.html', {'listings': listings, 'search_query': request.GET.get('search', '')})

#Just a try
def filter_hotel_view(request,filter_value):
    print("The filter value is:",filter_value)
    filters = Filter.objects.all()
    if filter_value:
        listings = Listing.objects.filter(filters__name=filter_value)  # Assuming you have a ManyToMany relationship
    else:
        listings = Listing.objects.all()

    context = {'listings': listings,
               'filters':filters, 
               'search_query': request.GET.get('search', ''),
               'filter_value':filter_value,
               }
    return render(request, 'home.html',context )

@login_required
def update_listing(request, listing_id):
    # Retrieve the listing based on the ID
    listing = get_object_or_404(Listing, id=listing_id, hotel_owner=request.user)
    
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES, instance=listing)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your listing has been updated successfully!')
            return redirect('hotel_dashboard')
    else:
        form = ListingForm(instance=listing)

    return render(request, 'update_listing.html', {'form': form, 'listing': listing})

@login_required
def delete_listing(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id, hotel_owner=request.user)

    if request.method == 'POST':
        listing.delete()
        messages.success(request, 'Your listing has been deleted successfully!')
        return redirect('hotel_dashboard')

    return render(request, 'delete_listing.html', {'listing': listing})

@login_required
def edit_user(request):
    if request.method == 'POST':
        user = request.user
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')
        stay_logged_in = request.POST.get('stay_logged_in') == 'true'

        # Update user details
        user.username = username
        user.email = email

        if password:
            if password == confirm_password:
                user.set_password(password)
                user.save()
                if stay_logged_in:
                    update_session_auth_hash(request, user)
                messages.success(request, 'Your password has been changed successfully.')
            else:
                messages.error(request, 'Passwords do not match.')
        else:
            user.save()
            messages.success(request, 'Your profile has been updated successfully.')

        return redirect('edit_user')

    return render(request, 'edit_user.html')