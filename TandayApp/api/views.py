from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UserUpdateForm, BookingForm
from django.contrib import messages
from .models import Booking
from django.http import JsonResponse

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

@login_required
def home_view(request):
    username = request.session.get('username', 'Guest')
    return render(request, 'home.html', {'username': username})

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

        return redirect('hotel_login')

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


