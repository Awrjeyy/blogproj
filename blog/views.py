from django.shortcuts import render
from django.views import generic
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy, reverse
from django.views.generic.base import TemplateView
from .models import Post
# Create your views here.

class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'blog/index.html'


# class PostList(TemplateView):
#     # import pdb; pdb.set_trace()
   
#     template_name = 'users/index.html'

#     def get(self, request):
#         import pdb; pdb.set_trace()
#         queryset = Post.objects.filter(status=1).order_by('-created_on')
#         context = {
#             'title':Post.title,
#             'author':Post.author,
#             'content':Post.content
#         }
#         return render(request, self.template_name, context)
    

class PostDetail(generic.DetailView):
    model = Post
    # import pdb; pdb.set_trace()
    template_name = 'blog/detail.html'