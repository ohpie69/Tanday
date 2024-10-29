from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UserUpdateForm, Booking
from django.contrib import messages
from .models import Booking

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
        if user is not None and user.is_hotel:  
            login(request, user)
            return redirect('hotel_home')  
        else:
            error_message = "Incorrect username or password. Please try again."
            return render(request, 'hotel_login.html', {'error': error_message})
    return render(request, 'hotel_login.html')

def home_view(request):
    username = request.session.get('username', 'Guest')  # Get username from session, default to 'Guest'
    return render(request, 'home.html', {'username': username})

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()  # Save the user using the form's save method
                login(request, user)  # Log the user in after registration
                return redirect('home')  # Redirect to home after successful registration
            except Exception as e:
                print(f"Error saving user: {e}")  # Log the error
        else:
            print(form.errors)  # Log validation errors
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def hotel_registration_view(request):
    if request.method == "POST":
        # Get the form data from POST request
        hotel_name = request.POST.get("hotelName")
        location = request.POST.get("location")
        phone = request.POST.get("phone")
        description = request.POST.get("hotelDescription")
        owner_name = request.POST.get("ownerName")
        owner_email = request.POST.get("ownerEmail")
        owner_phone = request.POST.get("ownerPhone")
        manager_name = request.POST.get("managerName", "")
        manager_email = request.POST.get("managerEmail", "")
        manager_phone = request.POST.get("managerPhone", "")
        username = request.POST.get("username")
        password = request.POST.get("password")
        security_question = request.POST.get("securityQuestion")

        # Process the data (e.g., save it to the database)
        # Example: You could save this information to a database model
        # Hotel.objects.create(...)

        messages.success(request, "Registration successful! You can now log in.")

        # Redirect to the login page
        return redirect('hotel_login')

    # If GET request, render the form
    return render(request, 'hotel_register.html')

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
        'email': request.user.email  # Pass the user's email to the template
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
                'email': email,  # Retain the email input
                'name': name,    # Retain the name input
                'check_in': check_in,  # Retain the check-in date
                'check_out': check_out,  # Retain the check-out date
                'guests': guests,  # Retain the number of guests
                'room_types': room_types  # Retain the selected room types
            })

        # Create a new booking instance
        booking = Booking(
            user=request.user,  # Store the logged-in user
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
    
def success(request):
    return render(request, 'success.html')

def landing_page_view(request):
    return render(request, 'landingpage.html')

@login_required
def my_bookings(request):
    # Get all bookings for the logged-in user
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'my_bookings.html', {'bookings': bookings})
