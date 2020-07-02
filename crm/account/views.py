from django.shortcuts import render,redirect
from .forms import CustomerForm,OrderForm
from .models import Customer,Product,Order
from django.views import generic
from django.http import JsonResponse
from django.template.loader import render_to_string

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