from django.urls import path
from .views import customerView,customerCreateView,game

urlpatterns = [
    path('customers/',customerView,name='customers'),
    path('customers/create/',customerCreateView,name='customer-create'),
    path('game/',game,name='game')
]