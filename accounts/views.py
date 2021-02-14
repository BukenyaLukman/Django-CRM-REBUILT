from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

from django.http import HttpResponse
from django.forms import inlineformset_factory
from .forms import OrderForm,CreateUserForm
from .filters import OrderFilter

from django.contrib.auth import authenticate, login, logout

from . models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required




def registerPage(request):
	form = CreateUserForm()

	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			form.save()
			user = form.cleaned_data.get('username')
			messages.success(request, 'Account was created for ' + user)
			return redirect('accounts:login')
	context = {'form':form}
	return render(request, 'accounts/register.html', context)

def loginPage(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request,user)
			return redirect('accounts:home')
		else:
			messages.info(request, 'Username or Password incorrect')
	context = {}
	return render(request, 'accounts/login.html', context)




def logoutUser(request):
	logout(request)
	return redirect('accounts:login')



@login_required(login_url='login')
def home(request):
	orders = Order.objects.all()
	customers = Customer.objects.all()

	total_customers = customers.count()
	total_orders = orders.count()

	pending = orders.filter(status='Pending').count()
	delivered = orders.filter(status='Delivered').count()

	context = {
		'orders':orders,
		'customers':customers,
		'total_orders':total_orders,
		'delivered':delivered,
		'pending':pending,
	}
	return render(request, 'accounts/dashboard.html', context)

@login_required()
def products(request):
	products = Product.objects.all()
	context = {
		'products':products,
	}
	return render(request, 'accounts/products.html', context)
@login_required()
def customer(request, pk):
	customer = Customer.objects.get(id=pk)
	orders = customer.order_set.all()
	total_orders = orders.count()


	myFilter = OrderFilter(request.GET, queryset=orders)
	orders = myFilter.qs
	context = {
		'customer':customer,
		'orders':orders,
		'total_orders':total_orders,
		'myFilter':myFilter,
	}
	return render(request, 'accounts/customer.html',context)

@login_required()
def createOrder(request, pk):
	OrderFormSet = inlineformset_factory(Customer, Order, fields=('product','status'))

	customer = Customer.objects.get(id=pk)
	# form = OrderForm(initial={'customer':customer})
	formset = OrderFormSet(instance=customer)
	if request.method == 'POST':
		print('Printing POST', request.POST)
		# form = OrderForm(request.POST)
		formset = OrderFormSet(request.POST,instance=customer)
		if formset.is_valid():
			formset.save()
			return redirect("accounts:home")
	context = {

		'formset': formset,
		# 'customer':customer,
	}
	return render(request, 'accounts/order_form.html', context)


@login_required()
def updateOrder(request,pk):
	order = Order.objects.get(id=pk)
	form = OrderForm(instance=order)

	if request.method == 'POST':
		form = OrderForm(request.POST,instance=order)
		if form.is_valid():
			form.save()
	context ={
		'form':form,
	}
	return render(request, 'accounts/order_form.html',context)

@login_required()
def deleteOrder(request, pk):
	context = {
		
	}
	return render(request, 'accounts/delete.html', context)