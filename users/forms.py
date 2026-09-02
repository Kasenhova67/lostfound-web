from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, itemlostfull, itemfoundfull


class RegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']


# Формы для полных моделей (используются в lost/views.py)
class lostfullform(forms.ModelForm):
    product_title = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Title'}))
    place = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder': 'Lost this thing near'}))
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Date")
    time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), label="Time")
    description = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Description'}))
    contactme = forms.CharField(max_length=150, label="Contact", widget=forms.TextInput(attrs={'placeholder': 'Contact'}))
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Your username (optional)'}), required=False)

    class Meta:
        model = itemlostfull
        fields = ['product_title', 'place', 'date', 'time', 'description', 'contactme', 'username']


class foundfullform(forms.ModelForm):
    product_title = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Title'}))
    place = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder': 'Found this thing near'}))
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Date")
    time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), label="Time")
    description = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Description'}))
    contactme = forms.CharField(max_length=150, label="Contact", widget=forms.TextInput(attrs={'placeholder': 'Contact'}))
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Your username (optional)'}), required=False)

    class Meta:
        model = itemfoundfull
        fields = ['product_title', 'place', 'date', 'time', 'description', 'contactme', 'username']
