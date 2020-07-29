from django.urls import path
from .views import (
    ProfileListApiView,
    ProfileDetailUpdateDeleteView,
    PostListCreateView,
    PostDetailUpdateDeleteView,
    CommentUpdateDeleteView,
    CommentCreateView,
    FollowingCreateView,
    FollowingDeleteView
)

urlpatterns = [
    path('profiles/',ProfileListApiView.as_view()),
    path('profiles/<uuid:id>/',ProfileDetailUpdateDeleteView.as_view()),
    path('posts/',PostListCreateView.as_view()),
    path('posts/<int:pk>/',PostDetailUpdateDeleteView.as_view()),
    path('comments/<int:pk>/',CommentUpdateDeleteView.as_view()),
    path('comments/',CommentCreateView.as_view()),
    path('following/',FollowingCreateView.as_view()),
    path('following/<int:pk>/',FollowingDeleteView.as_view())
]