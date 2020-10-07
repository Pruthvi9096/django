from django import forms
from .models import Opportunity,Template,LineItem

class OpportunityForm(forms.ModelForm):
    class Meta:
        model = Opportunity
        fields = '__all__'

class TemplateForm(forms.ModelForm):
    class Meta:
        model = Template
        fields = '__all__'

class LineItemForm(forms.ModelForm):
    class Meta:
        model = LineItem
        fields = '__all__'