from django.db.models import Q
from rest_framework import views
from rest_framework import generics
from rest_framework.decorators import api_view,APIView,permission_classes
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from .serializers import (
    ProfileSerializer,
    PostSerializer,
    CommentSerializer,
    FollowingSerializer,
    GetFollowerSerializer,
    GetFollowingSerializer,
    UserProfileSerializer,
    UserCreateSerializer,
    UserLoginSerializer,
    OnlyProfileSerializer
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
    RetrieveDestroyAPIView,
    RetrieveAPIView
    
)
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .paginations import CustomPagination
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework import viewsets
from rest_framework.decorators import action

class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = OnlyProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = [AllowAny]

    @action(detail=True,url_path='posts',url_name="profile-posts")
    def posts(self,request,*args,**kwargs):
        queryset = self.get_object().post_set.all()
        serializer = PostSerializer(queryset,many=True)
        return Response(serializer.data)
    
    @action(detail=True,url_path='posts/(?P<post_pk>[^/.]+)/comments',url_name='post-commets')
    def comments(self,request,*args,**kwargs):
        queryset = Comments.objects.filter(post_id=self.kwargs.get('post_pk'))
        serializer = CommentSerializer(queryset,many=True)
        return Response(serializer.data)

class UserRegistrationView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer

class UserLoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self,request,*args,**kwargs):
        data = request.data
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid():
            new_data = serializer.data
            return Response(new_data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class UserAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer

class ProfileListApiView(generics.ListAPIView):
    queryset = Profile.objects.all().order_by('user_id')
    serializer_class = ProfileSerializer
    pagination_class = CustomPagination
    filter_backends = [SearchFilter]
    search_fields = ['user__username','user__first_name','user__last_name','user__email']

class ProfileDetailUpdateDeleteView(RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'id'

class PostListCreateView(ListCreateAPIView):
    queryset = Post.objects.all().order_by('-date_created')
    serializer_class = PostSerializer
    pagination_class = CustomPagination
    filter_backends = [SearchFilter]
    search_fields = ['title','content','author__user__username',
        'author__user__first_name','author__user__last_name','date_created']

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
    query = request.GET.get('search',False)
    profile = Profile.objects.get(id=id)
    if profile.user == request.user or profile.mode == 'public':
        paginator = PageNumberPagination()
        paginator.page_size = 10
        users = Following.objects.filter(target=profile.user)
        if query:
            users = users.filter(
                Q(follower__username__icontains=query) |
                Q(follower__first_name__icontains=query) |
                Q(follower__last_name__icontains=query) 
            )
        result_page = paginator.paginate_queryset(users, request)
        serializer = GetFollowerSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    else:
        return Response({"message:Profile is private"},status=status.HTTP_200_OK)

@api_view(['GET'])
def get_following_list_api_view(request,id):
    query = request.GET.get('search',False)
    profile = Profile.objects.get(id=id)
    if profile.user == request.user or profile.mode == 'public':
        paginator = PageNumberPagination()
        paginator.page_size = 10
        users = Following.objects.filter(follower=profile.user)
        if query:
            users = users.filter(
                Q(target__username__icontains=query) |
                Q(target__first_name__icontains=query) |
                Q(target__last_name__icontains=query) 
            )
        result_page = paginator.paginate_queryset(users, request)
        serializer = GetFollowingSerializer(result_page,many=True)
        return paginator.get_paginated_response(serializer.data)
    else:
        return Response({"message:Profile is private"},status=status.HTTP_200_OK)

@api_view(['GET'])
def get_post_list_api_view(request,id):
    query = request.GET.get('search',False)
    profile = Profile.objects.select_related('user').get(id=id)
    if profile.user == request.user or profile.mode == 'public':
        paginator = PageNumberPagination()
        paginator.page_size = 10
        posts = profile.post_set.all()
        if query:
            posts = posts.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(author__user__username__icontains=query) |
                Q(author__user__first_name__icontains=query) |
                Q(author__user__last_name__icontains=query) 
            )
        result_page = paginator.paginate_queryset(posts, request)
        serializer = PostSerializer(result_page,many=True,context={'request':request})
        return paginator.get_paginated_response(serializer.data)
    else:
        return Response({"message:Profile is private"},status=status.HTTP_200_OK)