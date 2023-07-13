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


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photo']

class CreateOrderForm(forms.ModelForm):
    class Meta:
        day = forms.DateTimeField(widget=forms.SelectDateWidget())
        time = forms.DateTimeField(widget=forms.SelectDateWidget())

        model = Orders
        fields = ['service_name', 'summary', 'barber', 'day', 'time', 'booker']
        widgets = {
            'barber': forms.HiddenInput(),
            'booker': forms.HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        self.barber = kwargs.pop('barber', None)
        self.booker = kwargs.pop('booker', None)
        super().__init__(*args, **kwargs)
        self.fields['barber'].initial = self.barber
        self.fields['booker'].initial = self.booker

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.reader = self.booker
        if commit:
            instance.save()
        return instance