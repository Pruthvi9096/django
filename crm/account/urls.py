from django.urls import path
from . import views

urlpatterns = [
   path('',views.DashboardView,name="dashboard"),
   path('update/<int:id>',views.updateOrder,name='update-order'),
   path('saveorder/<int:id>',views.saveOrder,name='save-order'),
   path('delete_order/<int:id>',views.deleteOrder,name='delete-order')
]
