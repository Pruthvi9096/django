from django.urls import path
from .views import (
    mainListCreateView,
    mainDetailUpdateDeleteView,
    attributeListCreateView,
    attributeDetailUpdateDeleteView,
)

urlpatterns = [
    path('mains',mainListCreateView.as_view()),
    path('mains/<int:pk>/',mainDetailUpdateDeleteView.as_view()),
    path('attributes/',attributeListCreateView.as_view()),
    path('attributes/',attributeDetailUpdateDeleteView.as_view()),
]