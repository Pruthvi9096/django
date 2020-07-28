from django.urls import path
from .views import (customerView,customerCreateView,game,getUpdateDeleteCustomer,productListCreateView,
productView,productDetailView,OrderListCreateView,OrderRetrieveUpdateDestroyAPIView,HealthDetailView)

urlpatterns = [
    path('customers/',customerView,name='customers'),
    path('customers/create/',customerCreateView,name='customer-create'),
    path('customer/<int:pk>/',getUpdateDeleteCustomer),
    path('products/',productView),
    path('products/class',productListCreateView.as_view()),
    path('product/<int:pk>/',productDetailView.as_view()),
    path('orders/',OrderListCreateView.as_view()),
    path('order/<int:pk>/',OrderRetrieveUpdateDestroyAPIView.as_view()),
    path('game/',game,name='game'),
    path('health-detail/<int:id>/',HealthDetailView.as_view({
    'get': 'retrieve'}),name='health-detail')
]