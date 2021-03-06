from pyexpat.errors import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.views import generic
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.views.generic.base import TemplateView
from django.core.paginator import Paginator

from blog.forms import CommentForm, CreatePostForm, UpdateForm
from users.models import CustomUser
from .models import Post, Comment
# Create your views here.

# class PostList(generic.ListView):
#     queryset = Post.objects.filter(status=1).order_by('-created_on')
#     template_name = 'blog/index.html'


def LikeView(request, id):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))#gets the post
    isliked = False
    if post.likes.filter(id=request.user.id).exists():#checks if the user liked the post
        post.likes.remove(request.user)#if yes unlike
        isliked = False
    else:
        post.likes.add(request.user)#if not then likes
        isliked = True
    return HttpResponseRedirect(reverse('blog:post_detail', args=[id]))#returns to specific post using after liking

def DeletePost(request, id):
    # import pdb; pdb.set_trace()
    post = Post.objects.get(id=id, author_id=request.user)
    if post.author_id == request.user.id:
        post_to_delete = post
        post_to_delete.delete()
    return HttpResponseRedirect(reverse('blog:index'))

class DeleteView(TemplateView):
    template_name='blog/delete.html'

    def get(self, request, id):
        post = get_object_or_404(Post, id=id)
        context = {
            'post':post
        }
        return render(request, 'blog/delete.html', context)
class PostList(TemplateView):
    # import pdb; pdb.set_trace()
   
    template_name = 'blog/index.html'

    def get(self, request):
        # import pdb; pdb.set_trace()
        
        context = Post.objects.all().order_by('-created_on')
        user_list = CustomUser.objects.all()
        p = Paginator(context, 5)  # creating a paginator object
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
        context_dict = {
            'context': context,
            'user_list': user_list,
            'page_obj': page_obj,
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
        post = get_object_or_404(Post, id=id)#grabs the post via post.id
        totallikes = post.total_likes()#since the likes is a ManyToManyFields then you can just do this and it will count
        user_list = CustomUser.objects.all()
        isliked = False
        form = CommentForm
        # import pdb; pdb.set_trace()
        comments = post.comment_set.all()
        if post.likes.filter(id=request.user.id).exists():
            isliked = True
        context = {'post':post,
                    'totallikes':totallikes,
                    'isliked':isliked,
                    'form':form,
                    'comments':comments,
                    'user_list': user_list
                    }

        return render(request, 
                    'blog/detail.html', 
                    context)

    def post(self, request, id):
        post = Post.objects.get(id=id)
        form = CommentForm(request.POST)
        # import pdb; pdb.set_trace()
        
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post_id = id
            comment.user_id = request.user.id
            comment.save()
            
            messages.success(request, f'You have posted a comment')
            return redirect('blog:post_detail',post.id)
        else:
            messages.error(request, f'Bruh')
            return redirect('blog:index')

            


class CreateView(TemplateView):
    form_class = CreatePostForm
    template_name = 'blog/create.html'
    

    def get(self, request):
        form = CreatePostForm
        return render(request, 'blog/create.html', {"form":form})

    def post(self, request):
        # import pdb; pdb.set_trace()
        
        form = CreatePostForm(request.POST, request.FILES)
        
       
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author=request.user
            blog.save()
            return HttpResponseRedirect(reverse('blog:index'))
            #form.save(commit=False), temporarily halts the save function until 
            #there is more to be added
        else:
            
            return render(request, 'blog/create.html', {'form':form})



class UpdateView(TemplateView):
    form_class = UpdateForm
            
    def get(self, request, id):
        # import pdb; pdb.set_trace()
        temp_post = id
        user_id = CustomUser.objects.get(id=request.user.id)
        post_id = Post.objects.get(author_id=user_id, id=temp_post)
        if post_id.author_id == request.user.id:
            post = Post.objects.filter(author_id=request.user).get(id=id)
            
            initial_data = {
                'title': post.title,
                'title_image': post.title_image,
                'content': post.content,
            }
            form = UpdateForm(initial=initial_data)
            context = {
                'form': form,
                'post': post,
            }
            return render(request,'blog/update.html', context)
        else:
            messages.error(request, "You're not the author of this post")
            return redirect('blog:index')

    def post(self, request, id):
        post = Post.objects.get(id=id, author_id=request.user)
        new_blog = UpdateForm(request.POST,
                                request.FILES,
                                instance=post)
        
        if new_blog.is_valid():
            new_blog.save()
            return redirect('blog:post_detail',post.id)
        else:
            initial_data = {
                'title': post.title,
                'title_image': post.title_image,
                'content': post.content,
            }
            new_blog = UpdateForm(initial_data)
            context = {
                'new_blog': new_blog,
                'post': post,
            }
        return render(request, 'blog/update.html', context)


