from rest_framework import views
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from .serializers import (
    ProfileSerializer,
    PostSerializer,
    CommentSerializer,
    FollowingSerializer,
    GetFollowerSerializer,
    GetFollowingSerializer,
)
from ..models import Profile,Post,Comments,Following,User
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    RetrieveUpdateAPIView,
    CreateAPIView,
    RetrieveDestroyAPIView
    
)

class ProfileListApiView(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class ProfileDetailUpdateDeleteView(RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'id'

class PostListCreateView(ListCreateAPIView):
    queryset = Post.objects.all().order_by('-date_created')
    serializer_class = PostSerializer

class PostDetailUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all().order_by('-date_created')
    serializer_class = PostSerializer

class CommentUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Comments.objects.all().order_by('-date_created')
    serializer_class = CommentSerializer

class CommentCreateView(CreateAPIView):
    queryset = Comments.objects.all().order_by('-date_created')
    serializer_class = CommentSerializer

class FollowingCreateView(CreateAPIView):
    queryset = Following.objects.all()
    serializer_class = FollowingSerializer

class FollowingDeleteView(RetrieveDestroyAPIView):
    queryset = Following.objects.all()
    serializer_class = FollowingSerializer

@api_view(['GET'])
def follow_api_view(request,target,follower):
    user = User.objects.select_related('profile').get(id=target)
    profile = user.profile
    following,created = Following.objects.get_or_create(target_id=target,follower_id=follower)
    if not profile.followers.filter(id=following.id).exists():
        profile.followers.add(following)
    return Response({"message:Follower added"},status=status.HTTP_200_OK)

@api_view(['GET'])
def unfollow_api_view(request,target,follower):
    user = User.objects.select_related('profile').get(id=target)
    profile = user.profile
    following = Following.objects.filter(target_id=target,follower_id=follower).first()
    if following and profile.followers.filter(id=following.id).exists():
        profile.followers.remove(following)
    return Response({"message:Follower removed"},status=status.HTTP_200_OK)

@api_view(['GET'])
def get_followers_list_api_view(request,id):
    profile = Profile.objects.get(id=id)
    if profile.user == request.user or profile.mode == 'public':

        users = Following.objects.filter(target=profile.user)
        serializer = GetFollowerSerializer(users,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    else:
        return Response({"message:Profile is private"},status=status.HTTP_200_OK)

@api_view(['GET'])
def get_following_list_api_view(request,id):
    profile = Profile.objects.get(id=id)
    if profile.user == request.user or profile.mode == 'public':

        users = Following.objects.filter(follower=profile.user)
        serializer = GetFollowingSerializer(users,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    else:
        return Response({"message:Profile is private"},status=status.HTTP_200_OK)

@api_view(['GET'])
def get_post_list_api_view(request,id):
    profile = Profile.objects.select_related('user').get(id=id)
    if profile.user == request.user or profile.mode == 'public':
        posts = profile.post_set.all()
        serializer = PostSerializer(posts,many=True,context={'request':request})
        return Response(serializer.data,status=status.HTTP_200_OK)
    else:
        return Response({"message:Profile is private"},status=status.HTTP_200_OK)