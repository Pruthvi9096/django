from django import forms
from .models import Opportunity,Template,LineItem,SaleProposal,OpportunityTemplates

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
    
    # def clean_max_discount(self):
    #     data = self.cleaned_data
    #     if data.get('discount_allowed') and not data.get('max_discount'):
    #         raise forms.ValidationError("Max Discount Required when discount is allowed")
    #     print(data)
    #     return data


class ProposalForm(forms.ModelForm):
    class Meta:
        model = SaleProposal
        exclude = ['created_on','created_by']
        widgets = {
            'valid_upto':forms.TextInput(attrs={'type':'date'})
        }