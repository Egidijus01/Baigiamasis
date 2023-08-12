from .models import Rating, Profile, Orders, Barber, Posts, Services
from django import forms
from django.contrib.auth.models import User
from django.forms import TextInput, FileInput, Textarea
from django.forms import SelectMultiple


class BarberReviewForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = 'rating', 'content', 'barber', 'reviewer'
        widgets = {
            'barber': forms.HiddenInput(),
            'reviewer': forms.HiddenInput(),
            'content': Textarea(attrs={
                    'class': "md-textarea form-control",
                    'rows': '3',
                
                    }),
          



        }

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Services
        fields = '__all__'


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photo']

class BarberForm(forms.ModelForm):
    class Meta:
        model = Barber
        fields = '__all__'
        exclude = ['email', 'user', 'login_name', 'group', 'services']
        
        widgets = {
            'name': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Vardas'
                }),
            'last_name': TextInput(attrs={
                'class': "form-control", 
                'style': 'max-width: 300px;',
                'placeholder': 'Pavarde'
                }),
            'about': TextInput(attrs={
                'class': "form-control", 
                'style': 'max-width: 300px;',
                'placeholder': 'Pavarde'
                }),
            'zipcode': TextInput(attrs={
                'class': "form-control", 
                'style': 'max-width: 300px;',
                'placeholder': 'Pavarde'
                }),
            'city': TextInput(attrs={
                'class': "form-control", 
                'style': 'max-width: 300px;',
                'placeholder': 'Pavarde'
                }),
            'country': TextInput(attrs={
                'class': "form-control", 
                'style': 'max-width: 300px;',
                'placeholder': 'Pavarde'
                }),
            'adress': TextInput(attrs={
                'class': "form-control", 
                'style': 'max-width: 300px;',
                'placeholder': 'Pavarde'
                }),
            'cover': FileInput(attrs={
                'class': "formFile mt-4", 
                'style': 'max-width: 300px;',
                'placeholder': 'Pavarde'
                })
        }



        # widgets = {
        #     'user': forms.HiddenInput(),
        #     'email': forms.HiddenInput(),
        #     'login_name': forms.HiddenInput(),

        #     'group': forms.HiddenInput(),
            


        # }

    def save(self, commit=True):
        instance = super().save(commit=False)

        user = self.cleaned_data.get('user')
        group = self.cleaned_data.get('group')

        if user and group:
            # Associate the user with the specified group
            user.groups.add(group)

        if commit:
            instance.save()
            self.save_m2m()

        return instance

class PostForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = 'hero', 'content', 'photo', 'author'
        widgets = {
            'author': forms.HiddenInput()

        }



