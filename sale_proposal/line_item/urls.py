from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('opportunity/',views.OpportunityView.as_view(),name='opportunity'),
    path('opportunity/create/',views.OpportunityCreate.as_view(),name='opportunity-create'),
    path('opportunity/<int:id>/',views.opportunity_detail_view, name="opportunity-detail"),
    path('templates/',views.TemplateView.as_view(),name='template'),
    path('template/create/',views.TemplateCreate.as_view(),name='template-create'),
    path('template/<int:id>/',views.template_detail_view, name="template-detail")
]