from django.shortcuts import render, redirect
from django.urls import reverse
from .models import (
    Opportunity, Template,
    LineItem, OpportunityTemplates, 
    TemplateLineItems, SaleProposal
)
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from .forms import (
    OpportunityForm, TemplateForm,
    LineItemForm, ProposalForm,
)
from django.forms import inlineformset_factory
from django.db.models import Count
from django.template.loader import render_to_string
from django.http import JsonResponse


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
    already_used_template = [line.template.id for line in OpportunityTemplates.objects.filter(opportunity=opportunity)]
    templates = Template.objects.exclude(id__in=already_used_template)
    for form in formset:
        form.fields['template'].queryset = templates
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
    already_used_line = [line.line_item.id for line in TemplateLineItems.objects.filter(template=template)]
    lines = LineItem.objects.exclude(id__in=already_used_line)
    for form in formset:
        form.fields['line_item'].queryset = lines
    if request.method == "POST":
        formset = FormSet(request.POST, instance=template)
        if formset.is_valid():
            formset.save()
            if request.is_ajax():
                html_form = render_to_string('frontend/template-form.html',context={'template': template, 'formset': formset},request=request)
                return JsonResponse({'form':html_form})
            return redirect(reverse('template-detail',kwargs={'id':template.id}))
    return render(request, 'frontend/template_detail.html', {'template': template, 'formset': formset})

class LineItemView(ListView):
    model = LineItem
    queryset = LineItem.objects.all()
    template_name = 'frontend/line_item.html'


class LineItemCreate(CreateView):
    model = LineItem
    queryset = LineItem.objects.all()
    template_name = 'frontend/line_create.html'
    form_class = LineItemForm

    def get_success_url(self):
        return reverse('line-item', kwargs={})


class LineItemDetail(DetailView):
    model = LineItem
    template_name = 'frontend/line_item_detail.html'
    pk_url_kwarg = 'id'

class ProposalsList(ListView):
    model = SaleProposal
    queryset = SaleProposal.objects.all()
    template_name = 'frontend/proposals.html'

class ProposalCreate(CreateView):
    model = SaleProposal
    queryset = SaleProposal.objects.all()
    template_name = 'frontend/proposal_create.html'
    form_class = ProposalForm

    def get_success_url(self):
        return reverse('proposals', kwargs={})

def get_related_templates(request,id):
    opportunity = Opportunity.objects.get(id=id)
    templates = opportunity.templates.all()
    html_options = render_to_string('frontend/related_templates.html',context={'templates':templates},request=request)
    return JsonResponse({'data':html_options})