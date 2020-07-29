from rest_framework import views
from rest_framework import generics
from .serializers import (
    ProfileSerializer,
    PostSerializer,
    CommentSerializer,
    FollowingSerializer,
)
from ..models import Profile,Post,Comments,Following
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