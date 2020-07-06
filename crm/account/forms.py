from django import forms
from .models import Customer,Product,Order,Tag,Category
from ajax_select.fields import AutoCompleteSelectField, AutoCompleteSelectMultipleField
from ajax_select import make_ajax_field

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('name','email','phone')

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('customer','product','status')

class ProductForm(forms.ModelForm):
    tags = AutoCompleteSelectMultipleField('tags', required=False, help_text=None,plugin_options={'autoFocus': True, 'minLength': 1})
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['date_created']
        widgets = {
          'description': forms.Textarea(attrs={'rows':2, 'cols':15}),
          'tags':forms.TextInput(attrs={'placeholder':'Enter text to seach tags'})
        }