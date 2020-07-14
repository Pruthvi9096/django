from django.urls import path
from .views import (customerView,customerCreateView,game,getUpdateDeleteCustomer,productListCreateView,
productView)

urlpatterns = [
    path('customers/',customerView,name='customers'),
    path('customers/create/',customerCreateView,name='customer-create'),
    path('customer/<int:pk>/',getUpdateDeleteCustomer),
    path('products/',productView),
    path('game/',game,name='game')
]