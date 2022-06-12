from django.urls import path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from . import views

app_name = 'users'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path("pword_reset", views.password_reset_request, name="pword_reset"),
    path('pword_reset_done/', 
        auth_views.PasswordResetDoneView.as_view(template_name='users/pword_reset_done.html'), 
        name='pword_reset_done'),
    path('reset/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(template_name="users/pword_reset_confirm.html"), 
        name='pword_reset_confirm'),
    path('reset/done/', 
        auth_views.PasswordResetCompleteView.as_view(template_name='users/pword_reset_complete.html'), 
        name='pword_reset_complete'),
    path('change_password/', 
        views.change_password,
        name="change_password"),
    path('change_password_success', 
        views.PwordSuccess.as_view(),
        name='change_password_success'),   
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)