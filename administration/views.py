from .forms import OrderForm,TypeForm,ServiceForm,ProfileForm
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
from .models import Order,Type,Service,Profile,Assign
import datetime
import calendar
@login_required
def dashboard(request):
	icon = "pe-7s-graph icon-gradient bg-ripe-malin"
	title = "Dashboard"
	text = "Start here, you can check sumary of the sistem if you want you can push the review button."
	pos = "dashboard"
	breacum = []
	brea ={}
	brea["NAME"] = "Dashboard"
	brea["URL"] = "dashboard"
	brea["ICO"] = None
	brea["Active"] = True
	breacum.append(brea)
	brea ={}
	brea["NAME"] = "Home"
	brea["URL"] = "dashboard"
	brea["ICO"] = "pe-7s-home"
	brea["Active"] = None
	breacum.append(brea)
	today = datetime.datetime.now() 
	month = today.month 
	noorders=Order.objects.filter(State="active",Create__month = month).count()
	orders = Order.objects.filter(State="active")
	nopendingorders = Order.objects.filter(State="check").count()
	monts = [4,3,2,1,0]
	months = []
	for x in monts:
		m3 = {}
		m1 = int(2 - x)
		m2 = month+m1
		if(m2>12):
			m2=m2-12
		m3["month"] = calendar.month_name[m2]
		months.append(m3)
	Services = []
	Ser = Type.objects.all()
	Serv = []
	for s in Ser:
		p = {}
		p["service"] = s.Name
		Serv.append(p)
		for m in monts:
			se = {}
			se["service"] = s.Name
			se["color"] = s.color
			se["month"] = None
			se["Count"] = None
			m1 = int(2 - m)
			m2 = month+m1
			se["month"] = calendar.month_name[m2]
			se["Count"] = Service.objects.filter(Type=s,Create__month=m2).count()
			Services.append(se)
	return render(request, 'administration/dashboard.html',{'icon':icon,'title':title,'text':text,'pos':pos,'breacum':breacum,'noorders': noorders,'months':months,'Services':Services,'nopendingorders':nopendingorders,'Serv':Serv})
@login_required
def neworder(request):
	icon = "pe-7s-box2 icon-gradient bg-ripe-malin"
	title = "New Order"
	text = "Form of order, you can add only the order to check before."
	pos = "cnorder"
	breacum = []
	brea ={}
	brea["NAME"] = "New Order"
	brea["URL"] = "neworder"
	brea["ICO"] = None
	brea["Active"] = True
	breacum.append(brea)
	brea ={}
	brea["NAME"] = "Orders"
	brea["URL"] = "listorder"
	brea["ICO"] = "pe-7s-box2"
	brea["Active"] = None
	breacum.append(brea)
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
	return render(request, 'administration/create_new_order.html', {'icon':icon,'title':title,'pos':pos,'text':text,'breacum':breacum,'button': button,'form': form,'mensajes': mensajes,'errores': errores})
@login_required
def listorder(request):
	icon = "pe-7s-albums icon-gradient bg-ripe-malin"
	title = "List Order"
	text = "List of order, you can update or delete the orders."
	pos = "lorder"
	breacum = []
	brea ={}
	brea["NAME"] = "List of Orders"
	brea["URL"] = "listorder"
	brea["ICO"] = None
	brea["Active"] = True
	breacum.append(brea)
	brea ={}
	brea["NAME"] = "Orders"
	brea["URL"] = "listorder"
	brea["ICO"] = "pe-7s-box2"
	brea["Active"] = None
	breacum.append(brea)
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
	return render(request, 'administration/list_order.html', {'icon':icon,'title':title,'pos':pos,'text':text,'breacum':breacum,'orders': orders,'mensajes': mensajes,'errores': errores})
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
	request.session['mensajes']="The order has been Delete successfully"
	return redirect('listorder')
@login_required
def activeorder(request,pk):
	order=Order.objects.get(pk=pk)
	form = OrderForm(instance=order)
	post = form.save(commit=False)
	post.State = "active"
	post.save()
	request.session['mensajes']="The order has been active successfully"
	return redirect('addservice', pk=pk)
@login_required
def newservice(request, pk):
	errores=None
	mensajes=None
	types=None
	if request.method == "POST":
		form = TypeForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.color = request.POST["favcolor"]
			post.save()
			request.session['mensajes']="Se ha guardado con exito!"
			form = TypeForm()
		else:
			request.session['errores']="The type of service has been create before..."
	else:
		form = TypeForm()
		types=Type.objects.all()
	return redirect('addservice',pk=pk)
@login_required
def addservice(request, pk):
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
	types=None
	order=Order.objects.get(pk=pk)
	types=Type.objects.all()
	if request.method == "POST":
		try:
			for service in request.POST.getlist('Services'):
				form1 = ServiceForm(request.POST)
				if form1.is_valid():
					post = form1.save(commit=False)
					post.Order=order
					post.Type=Type.objects.get(Name=service)
					post.save()
					mensajes = "It has been saved successfully!"
				else:
					errores="It has NOT been saved successfully..."
		except Exception as e:
			errores="The type of service has been assign before..."
		
		form = TypeForm()
		form1 = ServiceForm()
	else:
		form = TypeForm()
		form1 = ServiceForm()
	return render(request, 'administration/add_services.html', {'order':order,'form': form,'form1': form1,'mensajes': mensajes,'errores': errores,'types': types})

@login_required
def listservice(request):
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
	Services = Service.objects.filter(State="Active")
	return render(request, 'administration/list_service.html', {'Services': Services,'mensajes': mensajes,'errores': errores,})
@login_required
def listservices(request):
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
	Services = []
	Orders=Order.objects.filter(State="active")
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
			Serv['Create']=y.Create
		Serv['Type']=tp
		Services.append(Serv)
	return render(request, 'administration/list_services.html', {'Services': Services,'mensajes': mensajes,'errores': errores,})
@login_required
def editservice(request, pk):
	Services=Service.objects.get(pk=pk)
	if request.method == "POST":
		form = ServiceForm(request.POST, instance=Services)
		if form.is_valid():
			post = form.save(commit=False)
			post.save()
			request.session['mensajes']="It has been edited successfully!"
			return redirect('listservice')
		else:
			request.session['errores']="No se ha podido guardar revise los campos para continuar..."
	else:
		form1 = ServiceForm(instance=Services)
	return render(request, 'administration/editservice.html', {'Services':Services,'form1':form1})
@login_required
def editservices(request, pk):
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

@login_required
def deleteservice(request,pk):
	service=Service.objects.get(pk=pk)
	service.delete()
	request.session['mensajes']="The Service has been Delete successfully"
	return redirect('listservice')
@login_required
def deleteservices(request,pk):
	try:
		order=Order.objects.get(pk=pk)
		Services=Service.objects.filter(Order=order)
		for serv in Services:
			serv.delete()
		request.session['mensajes']="The Services has been Delete successfully"
	except Exception as e:
		request.session['errores']="The services has NOT been saved successfully..."
	return redirect('listservices')
@login_required
def new_employee(request):
	errores=None
	mensajes=None
	button="New Employee"
	if request.method == "POST":
		form = ProfileForm(request.POST)
		if form.is_valid():
			if(request.POST['user']):
				try:
					usuario = User.objects.create_user(username=request.POST['user'],password="katarina123")
					post = form.save(commit=False)
					if(request.POST['user']):
						post.Usuario=User.objects.get(username=request.POST['user'])
					print(request.POST['user'])
					post.save()
					mensajes="It has been create successfully!!"
					form = ProfileForm()
				except Exception as e:
					errores="the user has been create before, if you want to asign the user please leave blank the space and assign it in configurations..."
				return render(request, 'administration/create_new_job.html', {'button': button,'form': form,'mensajes': mensajes,'errores': errores})
		else:
			errores="The Employee has NOT been saved successfully..."
	else:
		mensajes=None
		form = ProfileForm()
	return render(request, 'administration/create_new_job.html', {'button': button,'form': form,'mensajes': mensajes,'errores': errores})
