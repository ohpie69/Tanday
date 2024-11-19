from django import forms
from django.contrib.auth.models import User
from .models import Booking, Hotel

# User Registration Form
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
        help_texts = {
            'first_name': '',
            'last_name': '',
            'username': '',
            'email': '',
            'password': '',
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

# User Update Form
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

# Hotel Registration Form
class HotelRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}), 
        label="Password"
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}), 
        label="Confirm Password"
    )
    
    class Meta:
        model = Hotel
        fields = ['hotel_name', 'location', 'phone', 'hotel_description', 'username', 'email', 'password']
        widgets = {
            'hotel_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Hotel Name'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Location'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+65'}),
            'hotel_description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Hotel Description'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        }
        help_texts = {
            'hotel_name': '',
            'location': '',
            'phone': '',
            'hotel_description': '',
            'username': '',
            'email': '',
            'password': '',
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        # Validate that passwords match
        if password != password_confirm:
            raise forms.ValidationError("Passwords do not match")
        
        return cleaned_data

# Hotel Login Form
class HotelLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label="Username/Email")
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label="Password")

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

# Booking Form
ROOM_TYPE_CHOICES = [
    ('gaming-room', 'Gaming Room'),
    ('pool-area', 'Pool Area'),
    ('sunbed', 'Sunbed'),
    ('cabin', 'Cabin'),
    ('canoe', 'Canoe'),
    ('countryside', 'Countryside'),
    ('home', 'Home'),
    ('historic', 'Historic'),
]

class BookingForm(forms.ModelForm):
    room_types = forms.MultipleChoiceField(
        choices=ROOM_TYPE_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        label="Room Types"
    )

    class Meta:
        model = Booking
        fields = ['name', 'email', 'check_in', 'check_out', 'guests', 'room_types']
        widgets = {
            'check_in': forms.DateInput(attrs={'type': 'date'}),
            'check_out': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get('check_in')
        check_out = cleaned_data.get('check_out')

        # Check that check_out is after check_in
        if check_in and check_out and check_out <= check_in:
            raise forms.ValidationError("Check-out date must be after the check-in date.")

        return cleaned_data
