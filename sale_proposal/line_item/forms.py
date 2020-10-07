from django import forms
from .models import Opportunity,Template,LineItem,SaleProposal

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

class ProposalForm(forms.ModelForm):
    class Meta:
        model = SaleProposal
        exclude = ['created_on','created_by']
        widgets = {
            'valid_upto':forms.TextInput(attrs={'type':'date'})
        }