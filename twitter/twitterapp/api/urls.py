from django.urls import path,include
from .views import (
    ProfileListApiView,
    ProfileDetailUpdateDeleteView,
    PostListCreateView,
    PostDetailUpdateDeleteView,
    CommentUpdateDeleteView,
    CommentCreateView,
    FollowingCreateView,
    FollowingDeleteView,
    follow_api_view,
    unfollow_api_view,
    get_followers_list_api_view,
    get_following_list_api_view,
    get_post_list_api_view,
    UserAPIView,
    UserLoginView,
    UserRegistrationView,
    ProfileViewSet
    
)
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )
from rest_framework import routers
profile_router = routers.DefaultRouter()
profile_router.register('profile',ProfileViewSet,basename='profile')
from rest_framework.authtoken import views

urlpatterns = [
    path('',include(profile_router.urls)),
    path('login/',UserLoginView.as_view(),name='api-login'),
    path('register/',UserRegistrationView.as_view(),name='api-register'),
    path('api-token-auth/', views.obtain_auth_token, name='api-tokn-auth'),
    path('profiles/',ProfileListApiView.as_view()),
    path('profiles/<uuid:id>/',ProfileDetailUpdateDeleteView.as_view()),
    path('posts/',PostListCreateView.as_view()),
    path('posts/<int:pk>/',PostDetailUpdateDeleteView.as_view()),
    path('comments/<int:pk>/',CommentUpdateDeleteView.as_view()),
    path('comments/',CommentCreateView.as_view()),
    path('following/',FollowingCreateView.as_view()),
    path('following/<int:pk>/',FollowingDeleteView.as_view()),
    path('follow/<int:target>/<int:follower>/',follow_api_view),
    path('unfollow/<int:target>/<int:follower>/',unfollow_api_view),
    path('followerlist/<uuid:id>/',get_followers_list_api_view),
    path('followinglist/<uuid:id>/',get_following_list_api_view),
    path('postlist/<uuid:id>/',get_post_list_api_view),
    path('user/<int:pk>/',UserAPIView.as_view()),
    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]