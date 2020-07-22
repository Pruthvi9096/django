from django.urls import path
from . import views

urlpatterns = [
    path('',views.IndexView,name='index'),
    path('register/',views.RegisterView,name='register'),
    path('login/',views.LoginView,name='login'),
    path('logout/',views.LogoutView,name='logout'),
    path('update-profile',views.updateProfileView,name='update-profile')
]