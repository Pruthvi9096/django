from django.urls import path
from . import views

urlpatterns = [
    path('',views.orm_practice,name='orm')
]