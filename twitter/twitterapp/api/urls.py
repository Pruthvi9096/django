from django.urls import path
from .views import (
    ProfileListApiView,
    ProfileDetailUpdateDeleteView,
    PostListCreateView
)

urlpatterns = [
    path('profiles/',ProfileListApiView.as_view()),
    path('profiles/<uuid:id>/',ProfileDetailUpdateDeleteView.as_view()),
    path('posts/',PostListCreateView.as_view())
]