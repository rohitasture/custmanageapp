from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory

from .filters import OrderFilter
from .models import *
from .forms import OrderForm
# Create your views here.
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_customers = customers.count()

    total_orders = orders.count()
    delivered = orders.filter(status = 'Delivered').count()
    pending = orders.filter(status = 'Pending').count()

    context = { 'orders':orders, 'customers':customers, 'total_orders':total_orders, 'delivered': delivered, 'pending':pending }
    return render(request,'custmanageapp/dashboard.html',context)

def products(request):
    products = Product.objects.all()
    return render(request,'custmanageapp/products.html',{'products':products})

def customer(request, pk):
    customer = Customer.objects.get(id = pk)
    orders = customer.order_set.all()
    order_count = orders.count()

    myFilter = OrderFilter(request.GET, queryset = orders)
    orders = myFilter.qs
    context = {'customer':customer, 'orders':orders, 'order_count':order_count, 'myFilter': myFilter}
    return render(request,'custmanageapp/customer.html',context)

def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(Customer,Order, fields = ('product','status'), extra = 10)
    customer = Customer.objects.get(id = pk)
    #form = OrderForm(initial = {'customer': customer})
    formset = OrderFormSet(queryset = Order.objects.none() ,instance = customer)
    if request.method == 'POST':
        #form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance = customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {'formset':formset}
    return render(request,'custmanageapp/order_form.html',context)

def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance = order)
    if request.method == 'POST':
        form = OrderForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form':form}
    return render(request,'custmanageapp/order_form.html',context)

def deleteOrder(request,pk):
    order = Order.objects.get(id=pk)
    context = {'item':order}
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    return render(request,'custmanageapp/delete.html',context)
