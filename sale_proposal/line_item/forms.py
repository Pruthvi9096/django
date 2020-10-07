from django import forms
from .models import Opportunity,Template

class OpportunityForm(forms.ModelForm):
    class Meta:
        model = Opportunity
        fields = '__all__'

class TemplateForm(forms.ModelForm):
    class Meta:
        model = Template
        fields = '__all__'