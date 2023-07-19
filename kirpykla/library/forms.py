from .models import Rating, Profile, Orders
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
    email = User
    class Meta:
        model = User
        fields = ['username', 'email']


# class TimeSelectionForm(forms.ModelForm):
    
#     class Meta:
#         model = AvailableTimes
#         fields = ['day', 'time']

# class OrderSelectForm(forms.ModelForm):
    
#     class Meta:
#         model = Orders
#         fields = ['barber', 'service_name', 'summary', 'booker']

#         widgets = {
#             'barber': forms.HiddenInput(),
#             'booker': forms.HiddenInput()

#         }






class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photo']

