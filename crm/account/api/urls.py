from django.urls import path
from .views import (customerView,customerCreateView,game,getUpdateDeleteCustomer,productListCreateView,
productView,productDetailView)

urlpatterns = [
    path('customers/',customerView,name='customers'),
    path('customers/create/',customerCreateView,name='customer-create'),
    path('customer/<int:pk>/',getUpdateDeleteCustomer),
    path('products/',productView),
    path('products/class',productListCreateView.as_view()),
    path('product/<int:pk>/',productDetailView.as_view()),
    path('game/',game,name='game')
]