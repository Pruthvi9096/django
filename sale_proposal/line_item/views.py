from django.shortcuts import render, redirect
from django.urls import reverse
from .models import (
    Opportunity, Template,
    LineItem, OpportunityTemplates,
    TemplateLineItems, SaleProposal,
    OrderLine,Contact
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
import json
from django.db.models import QuerySet, F, Count


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
        Opportunity, OpportunityTemplates, fields=("template",), extra=1
    )
    formset = FormSet(
        queryset=OpportunityTemplates.objects.none(), instance=opportunity)
    already_used_template = [
        line.template.id for line in OpportunityTemplates.objects.filter(opportunity=opportunity)]
    templates = Template.objects.exclude(id__in=already_used_template)
    for form in formset:
        form.fields['template'].queryset = templates
    if request.method == "POST":
        formset = FormSet(request.POST, instance=opportunity)
        if formset.is_valid():
            formset.save()
            return redirect(reverse('opportunity-detail', kwargs={'id': opportunity.id}))
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
        Template, TemplateLineItems, fields=("line_item", "charge_category"), extra=1
    )
    formset = FormSet(
        queryset=TemplateLineItems.objects.none(), instance=template)
    already_used_line = [
        line.line_item.id for line in TemplateLineItems.objects.filter(template=template)]
    lines = LineItem.objects.exclude(id__in=already_used_line)
    for form in formset:
        form.fields['line_item'].queryset = lines
    if request.method == "POST":
        formset = FormSet(request.POST, instance=template)
        if formset.is_valid():
            formset.save()
            return redirect(reverse('template-detail', kwargs={'id': template.id}))
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
    
    def get_context_data(self,*args,**kwargs):
        context = super(ProposalCreate, self).get_context_data(*args, **kwargs)
        new_obj = SaleProposal.objects.create(name='New')
        context['form'].instance = new_obj
        context['sale_id'] = new_obj
        return context

def proposal_create(request):
    sale_id = request.GET.get('new',False)
    if sale_id:
        new_id = SaleProposal.objects.get(id=int(sale_id))
    else:
        new_id = SaleProposal.objects.create(name='New')
    form = ProposalForm(instance=new_id)
    order_lines = new_id.orderline_set.all()
    if request.method == 'POST':
        form = ProposalForm(request.POST, instance=new_id)
        if form.is_valid():
            form.save()
            return redirect(reverse('proposals'))
    return render(request,'frontend/proposal_create.html',{'form':form,'sale_id':new_id, 'order_line':order_lines})


def get_related_templates(request, id):
    opportunity = Opportunity.objects.get(id=id)
    templates = opportunity.templates.all()
    html_options = render_to_string(
        'frontend/related_templates.html', context={'templates': templates}, request=request)
    return JsonResponse({'data': html_options})


def generate_line_items(request, id):
    data = json.loads(request.body)
    sale_id = SaleProposal.objects.get(id=data.get('sale_id'))
    order_lines = [line.product.id for line in sale_id.orderline_set.all()]
    items = TemplateLineItems.objects.filter(template_id=id)
    # line_items = [line.line_item for line in items]
    line_item_page = render_to_string(
        'frontend/generate_line_items.html', context={'line_items': items, 'order_lines':order_lines}, request=request)
    return JsonResponse({'data': line_item_page})


def generate_order_lines(request):
    data = json.loads(request.body)
    lineitems = data.get('line_items')
    sale_id = SaleProposal.objects.get(id=data.get('sale_id'))
    sale_id.contact_for = Contact.objects.get(id=data.get('contact_for'))
    sale_id.attention_to = Contact.objects.get(id=data.get('attention_to'))
    sale_id.opportunity = Opportunity.objects.get(id=data.get('opportunity'))
    sale_id.template = Template.objects.get(id=data.get('template'))
    sale_id.valid_upto = data.get('valid_upto')
    sale_id.save()
    # line_items = LineItem.objects.filter(id__in=lineitems)
    results = TemplateLineItems.objects.filter(id__in=lineitems)
    # result = []
    order_lines = sale_id.orderline_set.all()
    product_lines = [line.product.id for line in order_lines]
    for line in results:
        if line.line_item.id not in product_lines:
            OrderLine.objects.create(
                proposal = sale_id,
                product = line.line_item,
                charge_category = line.charge_category,
                price = line.line_item.sale_price,
            )
    selected_products = [line.line_item.id for line in results]
    for order_line in order_lines:
        if order_line.product.id not in selected_products:
            order_line.delete()
            # result.append(order_line)
        # if line.charge_category:
        #     if line.charge_category.name not in result.keys():
        #         result[line.charge_category.name] = results.filter(
        #             charge_category=line.charge_category)
    # order_line_page = render_to_string(
    #     'frontend/generate_order_line.html', context={'order_line': result}, request=request)
    return JsonResponse({'data': True})
