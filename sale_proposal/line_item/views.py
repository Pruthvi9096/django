from django.shortcuts import render,redirect
from django.urls import reverse
from .models import Opportunity,Template,LineItem,OpportunityTemplates
from django.views.generic import ListView,DetailView
from django.views.generic.edit import CreateView
from .forms import OpportunityForm
from django.forms import inlineformset_factory

def index(request):
    return render(request,'frontend/dashboard.html',{})

class OpportunityView(ListView):
    model = Opportunity
    queryset = Opportunity.objects.all()
    template_name = 'frontend/opportunity.html'

class OpportunityCreate(CreateView):
    model = Opportunity
    queryset = Opportunity.objects.all()
    template_name = 'frontend/opportunity_create.html'
    form_class = OpportunityForm

    def get_success_url(self):
        return reverse('opportunity',kwargs={})

def opportunity_detail_view(request,id):
    opportunity = Opportunity.objects.get(id=id)
    FormSet = inlineformset_factory(
        Opportunity, OpportunityTemplates, fields=("template", "charge_category"), extra=1
    )
    formset = FormSet(queryset=OpportunityTemplates.objects.none(), instance=opportunity)
    if request.method == "POST":
        formset = FormSet(request.POST, instance=opportunity)
        if formset.is_valid():
            formset.save()
            return redirect("/")
    return render(request,'frontend/opportunity_detail.html'
        ,{'opportunity': opportunity,'formset':formset})