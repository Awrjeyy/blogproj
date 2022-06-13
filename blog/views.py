from pyexpat.errors import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.views import generic
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy, reverse
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.views.generic.base import TemplateView

from blog.forms import CreatePostForm, UpdateForm
from users.models import CustomUser
from .models import Post
# Create your views here.

# class PostList(generic.ListView):
#     queryset = Post.objects.filter(status=1).order_by('-created_on')
#     template_name = 'blog/index.html'


class PostList(TemplateView):
    # import pdb; pdb.set_trace()
   
    template_name = 'blog/index.html'

    def get(self, request):
        # import pdb; pdb.set_trace()
        context = Post.objects.all().order_by('-created_on')
        context_dict = {
            'context':context
        }
        return render(request, self.template_name, context_dict)
       
    

# class PostDetail(generic.DetailView):
#     model = Post
#     # import pdb; pdb.set_trace()
#     template_name = 'blog/detail.html'

class PostDetail(TemplateView):
    model = Post
    # import pdb; pdb.set_trace()
    template_name = 'blog/detail.html'
    
    def get(self, request, id):
        post = get_object_or_404(Post, id=id)
        return render(request, 'blog/detail.html', {'post':post})


class CreateView(TemplateView):
    form_class = CreatePostForm
    template_name = 'blog/create.html'
    

    def get(self, request):
        form = CreatePostForm
        return render(request, 'blog/create.html', {"form":form})

    def post(self, request):
        import pdb; pdb.set_trace()
        
        form = CreatePostForm(request.POST, request.FILES)
        
       
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author=request.user
            blog.save()
            return HttpResponseRedirect(reverse('blog:create_blog'))
            #form.save(commit=False), temporarily halts the save function until 
            #there is more to be added
        else:
            form = CreatePostForm(request.user)
        
        return render(request, 'blog/create_blog.html', {'form':form})

class UpdateView(TemplateView):
    form_class = UpdateForm        
    def get(self, request):
        form = UpdateForm
        return render(request,'blog/update.html',{'form':form})

    def post(self, request):
        up_form = request.user
        new_blog = UpdateForm(request.POST,
                                request.FILES,
                                instance=up_form)
        
        if new_blog.is_valid():
            new_blog.save()
            return HttpResponseRedirect(reverse('blog:update_blog'))
        else:
            new_blog = UpdateForm(request.user)
        return render(request, 'blog/update.html', {'new_blog':new_blog})

        # b_user = get_object_or_404(Post, author_id=request.user.id)
        # form = CreatePostForm(request.POST)
        # # import pdb; pdb.set_trace()
        # if request.method == 'POST':
            
        #     if form.is_valid():
        #         blog = form.save()
        #         return redirect('blog:index')

        # else:
        #     form = CreatePostForm(request.user.blog)
        
        # context = {
        #     'blog':blog
        # }

        # return render(request, 'blog/index.html', context)

# form = CreatePostForm(request.POST,
#                                 request.FILES,
#                                 instance=b_user)