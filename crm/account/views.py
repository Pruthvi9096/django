from django.shortcuts import render,redirect
from .forms import CustomerForm,OrderForm
from .models import Customer,Product,Order
from django.views import generic
from django.http import JsonResponse
from django.template.loader import render_to_string
from .filters import OrderFilter
from django.forms import inlineformset_factory
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator

def DashboardView(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('dashboard')
    else:
        form = CustomerForm()
    customers = Customer.objects.all().order_by('-id')
    total_orders = Order.objects.all().count()
    pending_orders = Order.objects.filter(status='pending').count()
    delivered_orders = Order.objects.filter(status='delivered').count()
    orders = Order.objects.all().order_by('-date_ordered')[:5]
    return render(request,'dashboard.html',{
        'form':form,
        'customers':customers,
        'orders':orders,
        'total_orders':total_orders,
        'pending_orders':pending_orders,
        'delivered_orders':delivered_orders})

def updateOrder(request,id):
    order = Order.objects.get(id=id)
    form = OrderForm(instance=order)
    context = {'orderform': form}
    html_form = render_to_string('account/order_form.html',
        context,
        request=request,
    )
    return JsonResponse({'form':html_form,'id':order.id})

def saveOrder(request,id):
    dict = {}
    order = Order.objects.get(id=id)
    if request.method == 'POST':
        form = OrderForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
            dict['is_form_valid'] = True
        else:
            dict['is_form_valid'] = False
    return JsonResponse(dict)

def deleteOrder(request,id):
    dict = {}
    order = Order.objects.get(id=id)
    order.delete()
    dict['deleted'] = True
    return JsonResponse(dict)

def customerView(request,slug):
    customer = Customer.objects.get(slug=slug)
    orders = customer.order_set.all().order_by('-date_ordered')
    order_count = orders.count()
    orderFilter = OrderFilter(request.GET,orders)
    orders = orderFilter.qs
    page = request.GET.get('page')
    paginator = Paginator(orders,5)
    try:
        orders = paginator.page(page)
    except PageNotAnInteger:
        orders = paginator.page(1)
    except EmptyPage:
        orders = paginator.page(orders.num_pages)
    context = {
        'customer':customer,'orders':orders,
        'order_count':order_count,
        'orderFilter':orderFilter}
    return render(request,'customer.html',context=context)

def createOrderView(request,id):
    customer = Customer.objects.get(id=id)
    OrderFormSet = inlineformset_factory(Customer,Order,fields=('product','status'),extra=1)
    formset = OrderFormSet(queryset=Order.objects.none(),instance=customer)
    if request.method == 'POST':
        formset = OrderFormSet(request.POST,instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('dashboard')
    return render(request,'account/create_order.html',{'formset':formset})

def updateCustomerView(request,id):
    customer = Customer.objects.get(id=id)
    form = CustomerForm(instance=customer)
    context = {'customerform':form}
    html_form = render_to_string('account/customer_form.html',context=context,request=request)
    return JsonResponse({'form':html_form,'id':customer.id})

def saveCustomerView(request,id):
    dict = {}
    customer = Customer.objects.get(id=id)
    print(request.method)
    if request.method == 'POST':
        form = CustomerForm(request.POST,instance=customer)
        if form.is_valid():
            form.save()
            dict['form_is_valid'] = True
        else:
            dict['form_is_valid'] = False
    return JsonResponse(dict)