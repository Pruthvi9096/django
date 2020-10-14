from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('opportunity/',views.OpportunityView.as_view(),name='opportunity'),
    path('opportunity/create/',views.OpportunityCreate.as_view(),name='opportunity-create'),
    path('opportunity/<int:id>/',views.opportunity_detail_view, name="opportunity-detail"),
    path('templates/',views.TemplateView.as_view(),name='template'),
    path('template/create/',views.TemplateCreate.as_view(),name='template-create'),
    path('template/<int:id>/',views.template_detail_view, name="template-detail"),
    path('line-item/',views.LineItemView.as_view(),name='line-item'),
    path('line-item/create/',views.LineItemCreate.as_view(),name='line-create'),
    path('line-item/<int:id>/',views.LineItemDetail.as_view(), name="line-item-detail"),
    path('proposals/',views.ProposalsList.as_view(),name='proposals'),
    path('proposal/<int:id>/',views.proposal_detail_view,name='proposal-detail'),
    path('proposal/create/',views.proposal_create, name='proposal-create'),
    path('get_related_templates/<int:id>/',views.get_related_templates),
    path('generate_line_items/<int:id>/',views.generate_line_items),
    path('generate_order_lines/',views.generate_order_lines)
]