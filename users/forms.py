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
    first_name = forms.CharField(label="First name", required=True, max_length=100, validators=[alpha], widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label="Last name", required=True, max_length=100, validators=[alpha], widget=forms.TextInput(attrs={'class': 'form-control'}))
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
    email = forms.CharField(label='Email', required=True, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}),
                            error_messages = {'required': 'Put an email',
                                                'invalid': 'Your Email Confirmation Not Equal With Your Email'})
    password = forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                            error_messages = {'required': 'Put a password',
                                            'invalid': 'Your Input a wrong Password'})

    field = (
        'email',
        'password'
    )
    
    
    def auth(self, request):
        import pdb; pdb.set_trace()
        auth_email = self.cleaned_data.get('email')
        pword = self.cleaned_data.get('password')
        email_qs = CustomUser.objects.filter(email=auth_email)
        if email_qs.count() == 0:
            raise  forms.ValidationError("The user does not exists")
        else:
            if auth_email and pword:
                user = authenticate(request, username=auth_email, password=pword)
                if not user:
                    raise forms.ValidationError('Incorrect Password')
        return super(LoginForm,self).auth(self, request)

        
    
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email is None:
            raise forms.ValidationError({'email': ["Put email."]})
        return email

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if password is None:
            raise forms.ValidationError({'password': ["Put password."]})
        return password
            






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
    bio = forms.CharField( widget=forms.Textarea, label="Bio", required=False)
    image = forms.ImageField(required=False)

    class Meta:
        model = Profile
        fields = (
            
            'bio',
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
