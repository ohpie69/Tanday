from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UserUpdateForm, BookingForm, HotelRegistrationForm, HotelLoginForm, ListingForm
from django.contrib import messages
from .models import Booking, Hotel, Listing, Filter
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.hashers import check_password
import logging

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
    listings = Listing.objects.all()  # Get all listings by default

    if search_query:
        # Filter listings by title or description
        listings = listings.filter(
            title__icontains=search_query
        ) | listings.filter(
            description__icontains=search_query
        )

    context = {
        'listings': listings,
        'search_query': search_query,
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
def booking_page(request):

    listing = Listing.objects.all()
    return render(request, 'booking.html', {
        'username': request.user.username,
        'email': request.user.email,  
        'listing':listing
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
        room_types = request.POST.getlist('room_type') 

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
                'room_types': room_types 
            })

        booking = Booking(
            user=request.user,
            name=name,
            email=email,
            check_in=check_in,
            check_out=check_out,
            guests=guests,
            room_types=', '.join(room_types) 
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
    
    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        
        if form.is_valid():
            # Save the form data back to the booking
            booking = form.save(commit=False)
            # Join room types to store as a comma-separated string
            booking.room_types = ','.join(form.cleaned_data['room_types'])
            booking.save()
            messages.success(request, 'Your booking has been updated successfully!')
            return redirect('my_bookings')  # Redirect to the bookings list page
    else:
        # Pre-fill room_types as a list for the form
        initial_data = booking.room_types.split(',') if booking.room_types else []
        form = BookingForm(instance=booking, initial={'room_types': initial_data})

    return render(request, 'edit_booking.html', {
        'form': form,
        'booking': booking,
        'room_types': form.fields['room_types'].choices
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
    listings = Listing.objects.all()
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
            return redirect('hotel_dashboard')
    else:
        form = ListingForm()

    return render(request, 'add_listing.html', {'form': form})

def listings_view(request):
    if request.method == 'GET':
        filter_name = request.GET.get('filter', None)
        if filter_name:
            # Filter listings based on the selected filter
            listings = Listing.objects.filter(filters__name=filter_name).values('id', 'title', 'description', 'price_per_night', 'image')
        else:
            # Fetch all listings if no filter is applied
            listings = Listing.objects.all().values('id', 'title', 'description', 'price_per_night', 'image')

        listings_list = list(listings)  # Convert QuerySet to a list
        return JsonResponse(listings_list, safe=False)

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