from dataclasses import fields
from multiprocessing import AuthenticationError
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import get_user_model
from django import forms
from .views import authenticate
from django.core.validators import RegexValidator
from .models import Profile, CustomUser


class RegisterForm(forms.ModelForm):
    alpha = RegexValidator(r'^[a-zA-Z]*$', 'Only alphabet characters are allowed.')
    first_name = forms.CharField(label="First name", required=True, max_length=100, validators=[alpha])
    last_name = forms.CharField(label="Last name", required=True, max_length=100, validators=[alpha])
    password1 = forms.CharField(label="Password", required=True, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="Confirm Password", required=True, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = CustomUser
        
        fields = (
            'email',
            'first_name',
            'last_name',

        )


class LoginForm(forms.Form):
    email = forms.CharField(label='Email', required=True, max_length=100)
    password = forms.CharField(label='Password',widget=forms.PasswordInput())

    field = (
        'email',
        'password'
    )
    def auth(self, request):
        # import pdb; pdb.set_trace()
        auth_email = self.cleaned_data.get('email')
        pword = self.cleaned_data.get('password')
        return authenticate(request, username=auth_email, password=pword)



class UserUpdate(forms.ModelForm):
    first_name = forms.CharField(label="First name", required=False, max_length=100)
    last_name = forms.CharField(label="Last name", required=False, max_length=100)

    class Meta:
        model = CustomUser
        fields = (
            'first_name',
            'last_name',

        )

class ProfileUpdate(forms.ModelForm):
    image = forms.ImageField(required=False)

    class Meta:
        model = Profile
        fields = (
            'image',

        )

class PWResetForm(forms.Form):
    email = forms.EmailField(
        label=("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email"}),
    )

class PWordChangeForm(forms.ModelForm):
    old_password = forms.CharField(label="Old Password", required=True, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="New Password", required=True, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="Confirm Password", required=True, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = CustomUser
        fields = (
            'old_password', 
            'password1',
            'password2',

        )
