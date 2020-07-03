from django import forms
from .models import Customer,Product,Order

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('name','email','phone')

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('customer','product','status')
