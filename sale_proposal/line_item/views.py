from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Opportunity, Template, LineItem, OpportunityTemplates, TemplateLineItems
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from .forms import OpportunityForm, TemplateForm
from django.forms import inlineformset_factory
from django.db.models import Count


def index(request):
    return render(request, 'frontend/dashboard.html', {})


class OpportunityView(ListView):
    model = Opportunity
    queryset = Opportunity.objects.annotate(
        template_count=Count('templates'))
    template_name = 'frontend/opportunity.html'


class OpportunityCreate(CreateView):
    model = Opportunity
    queryset = Opportunity.objects.all()
    template_name = 'frontend/opportunity_create.html'
    form_class = OpportunityForm

    def get_success_url(self):
        return reverse('opportunity', kwargs={})


def opportunity_detail_view(request, id):
    opportunity = Opportunity.objects.filter(id=id).annotate(
        template_count=Count('templates')).first()
    FormSet = inlineformset_factory(
        Opportunity, OpportunityTemplates, fields=("template", "charge_category"), extra=1
    )
    formset = FormSet(
        queryset=OpportunityTemplates.objects.none(), instance=opportunity)
    if request.method == "POST":
        formset = FormSet(request.POST, instance=opportunity)
        if formset.is_valid():
            formset.save()
            return redirect(reverse('opportunity-detail',kwargs={'id':opportunity.id}))
    return render(request, 'frontend/opportunity_detail.html', {'opportunity': opportunity, 'formset': formset})


class TemplateView(ListView):
    model = Template
    queryset = Template.objects.annotate(
        line_count=Count('line_items'))
    template_name = 'frontend/template.html'


class TemplateCreate(CreateView):
    model = Template
    queryset = Template.objects.all()
    template_name = 'frontend/template_create.html'
    form_class = TemplateForm

    def get_success_url(self):
        return reverse('template', kwargs={})


def template_detail_view(request, id):
    template = Template.objects.filter(id=id).annotate(
        line_count=Count('line_items')).first()
    FormSet = inlineformset_factory(
        Template, TemplateLineItems, fields=("line_item",), extra=1
    )
    formset = FormSet(
        queryset=TemplateLineItems.objects.none(), instance=template)
    if request.method == "POST":
        formset = FormSet(request.POST, instance=template)
        if formset.is_valid():
            formset.save()
            return redirect(reverse('template-detail',kwargs={'id':template.id}))
    return render(request, 'frontend/template_detail.html', {'template': template, 'formset': formset})