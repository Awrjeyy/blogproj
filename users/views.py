from pipes import Template
from turtle import update
import uuid
from django.core.mail import send_mail, BadHeaderError
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.encoding import force_bytes
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import views as auth_views
from django.views import generic
from django.urls import reverse_lazy, reverse
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.views.generic.base import TemplateView, View
from django.contrib import messages
from django.contrib.auth.decorators import login_required 
from .forms import  UserUpdate, ProfileUpdate, PWResetForm, PWordChangeForm
from .models import CustomUser, Profile
from django.utils.http import urlsafe_base64_encode
# Create your views here.

from .forms import LoginForm, RegisterForm

class IndexView(TemplateView):
    template_name = 'users/index.html'

    def get(self, request):
        return render(request, 'users/index.html')


class LoginView(TemplateView):#TemplateView
    
    template_name = 'users/login.html'

    def get(self, request):
        form = LoginForm
        return render(request, 'users/login.html', {"form":form})
    
    def post(self, request):
        form = LoginForm(request.POST)

        # import pdb; pdb.set_trace()
        if form.is_valid():
            username = request.POST['email']
            password = request.POST['password']

            user = authenticate(request, username=username, password=password)
            # import pdb; pdb.set_trace()
            if user is not None:
                login(request, user)
                return redirect('users:profile')
            else:
                form = LoginForm(request.POST)
                return render(request, 'users/login.html', {'form':form})
        else:
            return render(request, 'users/login.html', {'form':form})

class RegisterView(TemplateView):
    form_class = RegisterForm
    template_name = 'users/register.html'

    def get(self, request):
        form = RegisterForm
        return render(request, 'users/register.html', {"form":form})

    def post(self, request):
        form = RegisterForm(request.POST)
        # import pdb; pdb.set_trace()
        if form.is_valid():
            user = form.save()
            user.set_password(form.cleaned_data['password2'])
            user.save()
            username = request.POST['email']
            password = request.POST['password2']

            user = authenticate(request, username=username, password=password)
            messages.success(request, f'Your account has been created! You are now able to login.')

            return HttpResponseRedirect(reverse('users:login'))
        else:
            return render(request, 'users/register.html', {"form":form})

    
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('users:change_password_success')
        else:
            return render(request, 'users/change_password.html', {"form":form})
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'users/change_password.html', {"form":form})

class PwordSuccess(TemplateView):
    template_name = 'users/change_password_success.html'
    def get(self,request):
        return render(request, 'users/change_password_success.html')

#default_token_generator: will hash the values(3 values from the database 
# and the a value that is part of the token) and Django can verify it anytime
#force_bytes: if the string or data exists it will return a bytestring version of the object
#urlsafe_base64_encode: encodes the bytestring to a base64 string to use in URL
#bytestrings: holds true unicode characters in 8 bit bytes
#base64 string: convert binary to text data
def password_reset_request(request):
    password_reset_form = PWResetForm()
    if request.method == "POST":
        password_reset_form = PWResetForm(request.POST)
        if password_reset_form.is_valid():
            # import pdb; pdb.set_trace()
            data = password_reset_form.cleaned_data['email']
            associated_users = CustomUser.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    # import pdb; pdb.set_trace()
                    subject = "Password Reset Requested"
                    email_template_name = "users/password_reset_email.txt"
                    c = {
                        "email":user.email,
                        'domain':'127.0.0.1:8000',
                        'site_name':'Website',
                        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                        'user':user,
                        'token':default_token_generator.make_token(user),
                        'protocol':'http',

                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@example.com', [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid Header found.')
                    return redirect("users:pword_reset_done")
    form = PWResetForm()
    return render(request, template_name='users/pword_reset.html', context={'form':form})


# @login_required
class ProfileView(TemplateView):
    def get(self, request):
        if request.user.is_authenticated:
            user_form = UserUpdate
            profile_form = ProfileUpdate
            context = {
                'user_form':user_form,
                'profile_form':profile_form
            }
            return render(request, 'users/profile.html', context)
        else:
            return render(request, 'users.html')

    def post(self, request):
        #
        user = CustomUser.objects.get(id=request.user.id)
        #Model.objects.get((data in the model)=request.arguements/what is presented in the http/)
        p_user = Profile.objects.get(user_id=request.user.id)
        user_form = UserUpdate(request.POST, instance=user)
        profile_form = ProfileUpdate(request.POST,
                                        request.FILES,
                                        instance=p_user)
            
        # import pdb; pdb.set_trace()
        if request.method == 'POST':
            
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                messages.success(request, f'Account has been updated')
                return redirect('users:profile')
        else:
            # import pdb; pdb.set_trace()
            user_form = ProfileUpdate(request.user)
            profile_form = ProfileUpdate(request.user.profile)
            
        context = {
            'user_form':user_form,
            'profile_form':profile_form

        }

        return render(request, 'users/profile.html', context)

    




    #OLD CODES
    #   ----PwordChangeView---
        #class PwordChangeView
        # #form_class = PWordChangeForm
        # template_name = 'users/change_password.html'
        # def get(self, request):
        #     form = PWordChangeForm
        #     return render(request,'users/change_password.html', {"form":form})

        # def post(self, request):
        #     import pdb; pdb.set_trace()
        #     form = PWordChangeForm(request.POST)
        #     if form.is_valid():
        #         current_username = get_user
        #         user = form.save(commit=False)
        #         user.set_password(form.cleaned_data['password2'])
        #         user.save()
        #         username = current_username
        #         password = request.POST['password2']
        #         user = authenticate(request, username=username, password=password)
        #         return render(request, 'users/change_password_success.html') 
        #     else:
        #         return render(request,'users/change_password.html', {"form":form})