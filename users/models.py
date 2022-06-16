from asyncio.windows_events import NULL
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _ 
from .managers import CustomUserManager
from django.conf import settings
from django.db.models.signals import post_save
from PIL import Image
# Create your models here.


User = settings.AUTH_USER_MODEL
#The use of abstractuser is to remove username field and to use django user model
class CustomUser(AbstractUser):
    #Removes username field
    username = None
    #Makes the email field required and unique
    email = models.EmailField(_('email address'), unique=True)
    following = models.ManyToManyField(User, related_name="user_following")
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(default=NULL)
    image = models.ImageField(default='default.jpg',
        upload_to='profile_pics'
    )
    field = (
        'email',
        'password'
    )
    def __str__(self):
        return self.user.email
    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 100 or img.width > 100:
            new_img = (300, 300)
            img.thumbnail(new_img)
            img.save(self.image.path)
#Function create_profile and create_profile to save new register user by getting the users.id and register users.id it to profile database
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

def save_profile(sender, instance, **kwargs):
    instance.profile.save()

post_save.connect(create_profile, sender=User)
post_save.connect(save_profile, sender=User)