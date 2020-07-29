from django.urls import path
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
    get_following_list_api_view
)

urlpatterns = [
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
    path('followinglist/<uuid:id>/',get_following_list_api_view)
]