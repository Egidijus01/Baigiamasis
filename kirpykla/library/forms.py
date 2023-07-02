from .models import Rating
from django import forms


class BarberReviewForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = 'rating', 'content', 'barber', 'reviewer'
        widgets = {
            'barber': forms.HiddenInput(),
            'reviewer': forms.HiddenInput()

        }