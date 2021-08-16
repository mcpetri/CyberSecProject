from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Account, Message, Mail
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
import json

@login_required
@csrf_exempt 
def confirmView(request):

	amount = request.session['amount']
	to = User.objects.get(username=request.session['to'])

	request.user.account.balance -= amount
	to.account.balance += amount

	request.user.account.save()
	to.account.save()
	
	return redirect('/')
	

@login_required
@csrf_exempt 
def transferView(request):
	request.session['to'] = request.GET.get('to')
	request.session['amount'] = int(request.GET.get('amount'))
	return render(request, 'pages/confirm.html')

@csrf_exempt 
def mailView(request):
	Mail.objects.create(content=request.body.decode('utf-8'))
	print(request.body.decode('utf-8'))
	return HttpResponse('')


@csrf_exempt 
def addView(request):
	target = User.objects.get(username=request.POST.get('to'))
	Message.objects.create(source=request.user, target=target, content=request.POST.get('content'))
	return redirect('/')



@csrf_exempt 
def homePageView(request):
	messages = Message.objects.filter(Q(source=request.user) | Q(target=request.user))
	users = User.objects.exclude(pk=request.user.id)
	accounts = Account.objects.exclude(user_id=request.user.id)
	return render(request, 'pages/index.html', {'accounts': accounts,'msgs': messages, 'users': users})
