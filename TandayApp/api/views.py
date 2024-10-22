from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UserUpdateForm
from django.contrib import messages

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
    return render(request, 'home.html')

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user) 
            return redirect('home') 
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
    return render(request, 'booking.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')
