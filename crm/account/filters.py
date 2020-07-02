from django_filters import FilterSet
from .models import Order
from django_filters import DateFilter
from django.forms.widgets import DateInput 


class OrderFilter(FilterSet):
    start_date = DateFilter(
        field_name="date_ordered",lookup_expr='gte',widget=DateInput(attrs={'type':'date'}))
    end_date = DateFilter(
        field_name="date_ordered",lookup_expr='lte',widget=DateInput(attrs={'type':'date'}))
    class Meta:
        model = Order
        fields = ('product','status','start_date','end_date')
        
        