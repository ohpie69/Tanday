from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UserUpdateForm, BookingForm, HotelRegistrationForm, HotelLoginForm, ListingForm
from django.contrib import messages
from .models import Booking, Hotel, Listing, Filter
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.hashers import check_password

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
        form = HotelLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            # Authenticate the hotel using the custom Hotel model
            try:
                hotel = Hotel.objects.get(email=username)  # or use phone number, depending on your model
            except Hotel.DoesNotExist:
                hotel = None

            # Verify the password for the hotel
            if hotel and check_password(password, hotel.password):  # Assuming password is hashed
                login(request, hotel)  # Log the hotel in
                return redirect('hotel_dashboard')  # Adjust to your dashboard URL name
            else:
                messages.error(request, "Invalid username or password")

    else:
        form = HotelLoginForm()

    return render(request, 'hotel_login.html', {'form': form})

@login_required
def home_view(request):
    username = request.session.get('username', 'Guest')
    listings = Listing.objects.all()  # Fetch all listings
    return render(request, 'home.html', {'username': username, 'listings': listings})

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
            hotel_name = form.cleaned_data['hotel_name']
            location = form.cleaned_data['location']
            phone = form.cleaned_data['phone']
            hotel_description = form.cleaned_data['hotel_description']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Create hotel instance
            hotel = Hotel(
                hotel_name=hotel_name,
                location=location,
                phone=phone,
                hotel_description=hotel_description,
                username=username,
                email=email,
                password=password
            )
            hotel.save()

            return HttpResponse('Hotel registered successfully!')
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
    return render(request, 'booking.html', {
        'username': request.user.username,
        'email': request.user.email  
    })

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

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
    listings = Listing.objects.filter(hotel_owner=request.user)
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