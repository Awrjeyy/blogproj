from tkinter import CASCADE
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from PIL import Image
# Create your models here.

STATUS = (
    (0, "Draft"),
    (1, "Publish")
)
User = settings.AUTH_USER_MODEL
class Post(models.Model):
    title = models.CharField(max_length=255, unique=True)
    title_image = models.ImageField(blank=True, null=True, default='default_blog.jpg',
        upload_to='blog_pics'
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='blog_post')
    

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes.count()

    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.title_image.path)

        if img.height > 100 or img.width > 100:
            new_img = (750, 450)
            img.thumbnail(new_img)
            img.save(self.title_image.path)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta: 
        ordering = ['-created_on']

    def __str__(self):
        return 'Comment by {}'.format(self.user)