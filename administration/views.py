from .forms import OrderForm,TypeForm,ServiceForm
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import RequestContext, Template
from django.contrib.auth import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from .models import Order,Type,Service,Job,Profile,Assign
@login_required
def dashboard(request):
	noorders=Order.objects.filter(State="check").count()
	return render(request, 'administration/dashboard.html',{'noorders': noorders})
@login_required
def neworder(request):
	errores=None
	mensajes=None
	button="New Order"
	if request.method == "POST":
		form = OrderForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.save()
			mensajes="It has been create successfully!!"
			form = OrderForm()
		else:
			errores="No se ha podido guardar revise los campos para continuar..."
	else:
		mensajes=None
		form = OrderForm()
	return render(request, 'administration/create_new_order.html', {'button': button,'form': form,'mensajes': mensajes,'errores': errores})
@login_required
def listorder(request):
	orders = Order.objects.filter(State="active")
	try:
		mensajes = request.session['mensajes']
		del request.session['mensajes']
	except Exception as e:
		mensajes=None
	try:
		errores = request.session['errores']
		del request.session['errores']
	except Exception as e:
		errores=None
	return render(request, 'administration/list_order.html', {'orders': orders,'mensajes': mensajes,'errores': errores})
@login_required
def pendingorders(request):
	orders=Order.objects.filter(State="check")
	return render(request, 'administration/list_order.html',{'orders': orders})
@login_required
def editorder(request, pk):
	errores=None
	mensajes=None
	button="Edit Order"
	order=Order.objects.get(pk=pk)
	if request.method == "POST":
		form = OrderForm(request.POST, instance=order)
		if form.is_valid():
			post = form.save(commit=False)
			post.save()
			request.session['mensajes']="It has been edited successfully!"
			return redirect('listorder')
		else:
			request.session['errores']="No se ha podido guardar revise los campos para continuar..."
	else:
		form = OrderForm(instance=order)
	return render(request, 'administration/create_new_order.html', {'button': button,'form': form})
@login_required
def deleteorder(request,pk):
	order=Order.objects.get(pk=pk)
	form = OrderForm(instance=order)
	post = form.save(commit=False)
	post.State = "inactive"
	post.save()
	return redirect('listorder')
@login_required
def activeorder(request,pk):
	order=Order.objects.get(pk=pk)
	form = OrderForm(instance=order)
	post = form.save(commit=False)
	post.State = "active"
	post.save()
	request.session['mensajes']="The order has been active successfully"
	return redirect('listorder')
@login_required
def newservice(request, pk):
	errores=None
	mensajes=None
	types=None
	if request.method == "POST":
		form = TypeForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.save()
			mensajes="Se ha guardado con exito!"
			form = TypeForm()
		else:
			errores="No se ha podido guardar revise los campos para continuar..."
	else:
		form = TypeForm()
		types=Type.objects.all()
	return redirect('addservice',pk=pk)
@login_required
def addservice(request, pk):
	errores=None
	mensajes=None
	types=None
	order=Order.objects.get(pk=pk)
	types=Type.objects.all()
	if request.method == "POST":
		for service in request.POST.getlist('Services'):
			form1 = ServiceForm(request.POST)
			if form1.is_valid():
				post = form1.save(commit=False)
				post.Order=order
				post.Type=Type.objects.get(Name=service)
				post.save()
			else:
				errores="No se ha podido guardar revise los campos para continuar..."
		form = TypeForm()
		form1 = ServiceForm()
	else:
		form = TypeForm()
		form1 = ServiceForm()
	return render(request, 'administration/add_services.html', {'order':order,'form': form,'form1': form1,'mensajes': mensajes,'errores': errores,'types': types})

@login_required
def listservice(request):
	Services = Service.objects.all()
	return render(request, 'administration/list_service.html', {'Services': Services})
@login_required
def listservices(request):
	Services = []
	Orders=Order.objects.all()
	for x in Orders:
		Serv = {}
		Serv['pk']=x.pk
		Serv['Order']=str(x.pk) + "-" + x.Names + " " + x.Last_names
		types=Service.objects.filter(Order=x)
		tp=" "
		for y in types:
			tp=tp+" " + str(y.Type)
			Serv['Description']=str(y.Description)
			Serv['Note']=str(y.Note)
			Serv['Create']=str(y.Create)
		Serv['Type']=tp
		Services.append(Serv)
	return render(request, 'administration/list_services.html', {'Services': Services})
@login_required
def editservice(request, pk):
	Services=Service.objects.get(pk=pk)
	form1 = ServiceForm(instance=Services)
	return render(request, 'administration/editservice.html', {'Services':Services,'form1':form1})
@login_required
def editservices(request, pk):
	errores=None
	mensajes=None
	types=None
	order=Order.objects.get(pk=pk)
	typess=Type.objects.all()
	Services=Service.objects.filter(Order=order)
	types = []
	for x in typess:
		t = {}
		t['pk'] = x.pk
		t['Name'] = x.Name
		for y in Services:
			if y.Type==x:
				t['op'] = '1'
		types.append(t)
	if request.method == "POST":
		for serv in Services:
			serv.delete()
		servicelist = request.POST.getlist('Services')
		for service in servicelist:
			tp = Type.objects.get(Name=service)
			form1 = ServiceForm(request.POST)
			if form1.is_valid():
				post = form1.save(commit=False)
				post.Order = order
				post.Type = tp
				post.save()
			else:
				errores="No se ha podido guardar revise los campos para continuar..."
		return redirect('listservices')
	else:
		form = TypeForm()
		form1 = ServiceForm(instance=order)
	return render(request, 'administration/add_services.html', {'Services':Services,'order':order,'form': form,'form1': form1,'mensajes': mensajes,'errores': errores,'types': types})
