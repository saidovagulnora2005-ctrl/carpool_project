from django import forms
from .models import CustomUser
from .models import Trip, CompanionRequest
from django.contrib.auth.forms import UserChangeForm,UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email',)

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email',)


class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['start_location','end_location','date','seats_available','description']


class CompanionRequestForm(forms.ModelForm):
    class Meta:
        model = CompanionRequest
        fields = ['start_location','end_location','date','description']