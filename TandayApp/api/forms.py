from django import forms
from django.contrib.auth.models import User
from .models import Booking

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']  # Include email
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
        user.set_password(self.cleaned_data["password"])  # Hash the password
        if commit:
            user.save()
        return user

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']



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
    room_type = forms.MultipleChoiceField(
        choices=ROOM_TYPE_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        label="Room Types"
    )
    class Meta:
        model = Booking  # Assuming you have a Booking model
        fields = ['name', 'email', 'check_in', 'check_out', 'guests', 'room_type']
