from django.urls import path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from . import views
import users
app_name = 'blog'
urlpatterns = [
    path('', views.PostList.as_view(), name='index'),
    path('create_blog/', views.CreateView.as_view(), name='create_blog'),
    path('<int:id>/', views.PostDetail.as_view(), name='post_detail'),
    path('<int:id>/update_blog/', views.UpdateView.as_view(), name='update_blog'),
    path('<int:id>/like', views.LikeView, name='like_post'),
    path('<int:id>/delete_blog/', views.DeleteView.as_view(), name='delete_post'),
    path('<int:id>/delete_blog/confirm', views.DeletePost, name='delete_confirm'),
]
