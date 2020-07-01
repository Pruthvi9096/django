from django.urls import path
from . import views

urlpatterns = [
   path('',views.DashboardView,name="dashboard"),
   path('update/',views.updateOrder,name='update-order'),
   path('saveorder/',views.saveOrder,name='save-order')
]
