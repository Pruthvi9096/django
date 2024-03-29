from django.urls import path
from . import views

urlpatterns = [
   path('',views.DashboardView,name="dashboard"),
   path('login/',views.loginView,name='login'),
   path('signup/',views.signup,name='signup'),
   path('update/<int:id>',views.updateOrder,name='update-order'),
   path('saveorder/<int:id>',views.saveOrder,name='save-order'),
   path('delete_order/<int:id>',views.deleteOrder,name='delete-order'),
   path('customer/<slug:slug>',views.customerView,name='customer-detail'),
   path('create_order/<int:id>',views.createOrderView,name='create-order'),
   path('update_customer/<int:id>',views.updateCustomerView,name='update-customer'),
   path('save_customer/<int:id>',views.saveCustomerView,name='save-customer'),
   path('products/',views.ProductListView.as_view(),name='product-list'),
   path('products/create/',views.ProductCreateView.as_view(),name='product-create'),
   path('category-products/',views.category_product_api_view,name='category-products'),
   path('tag-products/',views.tag_product_api_view,name='tag-products'),
]
