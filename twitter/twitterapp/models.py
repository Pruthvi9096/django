from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
import uuid
from djrichtextfield.models import RichTextField
from datetime import datetime

from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.db.models import Count,Q

@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class Following(models.Model):
    target = models.ForeignKey(User,on_delete=models.CASCADE,related_name='followers')
    follower = models.ForeignKey(User,on_delete=models.CASCADE, related_name='targets')

class Profile(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_image = models.ImageField(upload_to='images/',null=True,blank=True)
    followers = models.ManyToManyField(Following,related_name='profiles')
    mode = models.CharField(max_length=50,choices=[('public','Public'),('private','Private')],default='public')

    def __str__(self):
        return self.user.username
    
    @property
    def get_followers(self):
        return [line.follower for line in self.followers.all().filter(target=self.user)]

    @property
    def follower_count(self):
        return Following.objects.filter(target=self.user).count()
    
    @property
    def following_count(self):
        return Following.objects.filter(follower=self.user).count()
    
    @property
    def post_count(self):
        return self.post_set.all().count()



class Post(models.Model):
    author = models.ForeignKey(Profile,on_delete=models.CASCADE,null=True)
    title = models.CharField(max_length=250,null=True)
    content = RichTextField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    @property
    def comment_count(self):
        return Post.objects.filter(id=self.id).aggregate(
            comment_count = Count('comments',filter=(
                Q(comments__parent_comment=None)
                ))
            )['comment_count']

    @property
    def like_count(self):
        return Post.objects.filter(id=self.id).aggregate(
            likes_count = Count('like')
        )['likes_count']

class Like(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    post = models.ForeignKey(Post,on_delete=models.CASCADE,null=True)
    date_created = models.DateTimeField(auto_now_add=True)

class Comments(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    post = models.ForeignKey(Post,on_delete=models.CASCADE,null=True)
    comment = models.TextField(max_length=2000,null=True)
    parent_comment = models.ForeignKey('Comments',on_delete=models.CASCADE,null=True,blank=True)
    date_created = models.DateTimeField(auto_now_add=True)


@receiver(post_save,sender=User)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save,sender=User)
def save_user_profile(sender,instance,**kwargs):
    instance.profile.save()
