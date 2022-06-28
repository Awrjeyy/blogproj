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
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import views as auth_views
from django.views import generic
from django.urls import reverse_lazy, reverse
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.views.generic.base import TemplateView, View
from django.contrib import messages
from django.contrib.auth.decorators import login_required 
from .forms import  UserUpdate, ProfileUpdate, PWResetForm, PWordChangeForm
from .models import CustomUser, Profile
from blog.models import Post
from django.utils.http import urlsafe_base64_encode
from django.core.paginator import Paginator

# Create your views here.

from .forms import LoginForm, RegisterForm

class SearchView(TemplateView):
    template_name = 'users/search_results.html'

    def get(self, request):
        # import pdb; pdb.set_trace()
        query = request.GET.get('q')
        filtered = request.GET.get('filter')
        object_list = {}
        if filtered == 'all':
            post_results = Post.objects.filter(
                Q(title__icontains=query) | Q(content__icontains=query)
            )
            user_results = CustomUser.objects.filter(
                Q(first_name__icontains=query) | Q(last_name__icontains=query)
            )
            crossref_profile = Profile.objects.all()
            object_list = {
                'post_results': post_results,
                'user_results': user_results,
                'crossref_profile': crossref_profile,
            }
        elif filtered == 'blog':
            post_results = Post.objects.filter(
                Q(title__icontains=query) | Q(content__icontains=query)
            )
            object_list = {
                'post_results': post_results,
            }
        elif filtered == 'profile':
            user_results = CustomUser.objects.filter(
                Q(first_name__icontains=query) | Q(last_name__icontains=query)
            )
            crossref_profile = Profile.objects.all()
            object_list = {
                'user_results': user_results,
                'crossref_profile': crossref_profile,
            }
        else:
            object_list = {}
        return render(request, self.template_name, object_list)

def FollowingView(request, id):
    # import pdb; pdb.set_trace()
    
    user = get_object_or_404(CustomUser, id=id)#the user's profile you are currently viewing
    p_id = Profile.objects.get(user_id=id)#this is for profile database just so you can grab profile.image
                                          # and bio or anything in there you need to post in html
    isFollowing = False
    if user.following.filter(id=request.user.id).exists():#this will check if logged in user is following the user you are viewing
        user.following.remove(request.user)
        isFollowing = False
    else:
        user.following.add(request.user)
        isFollowing = True
    return HttpResponseRedirect(reverse('users:profile', args=[p_id.id]))

            
    
class IndexView(TemplateView):
    template_name = 'users/index.html'

    def get(self, request):
        # import pdb; pdb.set_trace()
        profile_list = Profile.objects.all().order_by('-id')
        p = Paginator(profile_list, 5)  # creating a paginator object
        # getting the desired page number from url
        page_number = request.GET.get('page')
        
        try:
            page_obj = p.get_page(page_number)  # returns the desired page object
        except PageNotAnInteger:
            # if page_number is not an integer then assign the first page
            page_obj = p.page(1)
        except EmptyPage:
            # if page is empty then return last page
            page_obj = p.page(p.num_pages)
        user_list = CustomUser.objects.all()
        context = {
            'profile_list': profile_list,
            'user_list': user_list,
            'page_obj': page_obj
        }
        return render(request, self.template_name, context)


class LoginView(TemplateView):#TemplateView
    
    template_name = 'users/login.html'
    #gets the form and display in designated link
    def get(self, request):
        form = LoginForm
        return render(request, 'users/login.html', {"form":form})
    
    def post(self, request):
        form = LoginForm(request.POST)

        # import pdb; pdb.set_trace()
        if form.is_valid():
            username = request.POST['email']#grabs the field email and password
            password = request.POST['password']

            user = authenticate(request, username=username, password=password)
            # import pdb; pdb.set_trace()
            if user is not None:
                login(request, user)#if user is in the system will login and redirect
                return redirect('users:index')
            else:
                form = LoginForm(request.POST)
                return render(request, 'users/login.html', {'form':form})
        else:
            messages.error(request, "Unsuccessful registration. Invalid information.")
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
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password2'])
            user.save()
            username = request.POST['email']
            password = request.POST['password2']

            user = authenticate(request, username=username, password=password)
            messages.success(request, f'Your account has been created! You are now able to login.')

            return HttpResponseRedirect(reverse('users:login'))
        else:
            messages.error(request, "Unsuccessful registration. Invalid information.")
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
    def get(self, request, id):
        # import pdb; pdb.set_trace()
        logged_user = request.user.id#initialize the logged in user id
        temp_id = Profile.objects.get(user_id=id)#grabs the user_id from Profile database
        followers = CustomUser.objects.filter(user_following__id=temp_id.user_id)#profile.user_id will crossreference with users_following database
        following = CustomUser.objects.filter(following__id=temp_id.user_id)#trust me it looks funky so trial and error mode cuz it wont say
                                                                            #followers or following its going to be from_customuser_id and 
                                                                            #to_customuser_id
        totalfollowers = followers.count()
        totalfollowings = following.count()
        isFollowing = False
        if following.filter(id=logged_user).exists():
            isFollowing = True
        else:
            isFollowing = False
        p_user = Profile.objects.get(user_id=id)#Gets desired user's profile
        userid = CustomUser.objects.get(id=p_user.user_id)#Gets desired user's id
        totalfollowing = userid.following.count()
        post_list = Post.objects.filter(author_id=userid.id)
        context = {
            'following': following,
            'followers': followers,
            'totalfollowings': totalfollowings,
            'totalfollowers': totalfollowers,
            'isFollowing': isFollowing,
            'userid': userid,
            'p_user': p_user,
            'post_list': post_list,
        }
        return render(request, 'users/profile.html', context)
        

    

class UpdateProfileView(TemplateView):
    template_name = "users/update_profile.html"
    def get(self, request, id):
        p_user = Profile.objects.get(user_id=id)
        userid = CustomUser.objects.get(id=p_user.user_id)
        
        initial_userdata = {
            'first_name': userid.first_name,
            'last_name': userid.last_name,
        }
        initial_profdata = {
            'image': p_user.image,
            'bio': p_user.bio,
        }
        user_form = UserUpdate(initial_userdata)
        profile_form = ProfileUpdate(initial_profdata)
        context = {
            
            'profile_form': profile_form,
            'user_form': user_form,
            'userid': userid,
            'p_user': p_user,
            
        }
        return render(request, 'users/update_profile.html', context)

    def post(self, request, id):
        #
        user = CustomUser.objects.get(id=id)
        #Model.objects.get((data in the model)=request.arguements/what is presented in the http/)
        p_user = Profile.objects.get(user_id=id)
        user_form = UserUpdate(request.POST, instance=user)
        profile_form = ProfileUpdate(request.POST,
                                        request.FILES,
                                        instance=p_user)
            
        # import pdb; pdb.set_trace()
        
            
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f'Account has been updated')
            return HttpResponseRedirect(reverse('users:profile', args=[p_user.user_id]))

        else:
            # import pdb; pdb.set_trace()
            initial_userdata = {
                'first_name': user.first_name,
                'last_name': user.last_name,
            }
            initial_profdata = {
                'image': p_user.image,
                'bio': p_user.bio,
            }
            user_form = ProfileUpdate(initial_userdata)
            profile_form = ProfileUpdate(initial_profdata)
            
        context = {
            'user_form':user_form,
            'profile_form':profile_form

        }

        return render(request, 'users/update_profile.html', context)




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