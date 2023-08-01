from .models import Rating, Profile, Orders, Barber, Posts
from django import forms
from django.contrib.auth.models import User


class BarberReviewForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = 'rating', 'content', 'barber', 'reviewer'
        widgets = {
            'barber': forms.HiddenInput(),
            'reviewer': forms.HiddenInput()

        }

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']




class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photo']

class BarberForm(forms.ModelForm):
    class Meta:
        model = Barber
        fields = '__all__'

class PostForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = 'hero', 'content', 'photo', 'author'
        widgets = {
            'author': forms.HiddenInput()

        }