from django.shortcuts import render, redirect
from .models import Userentry
from django.core.urlresolvers import reverse
from django.contrib import messages


def index(request):
	return render(request, "login/index.html")

def checkandlogin(request):
    results = Userentry.objects.create_user(request.POST)
    if results[0] == True:
		request.session['name'] = results[1].name
		request.session['id'] = results[1].id
		return redirect('appointments:index')
    else:
        for err in results[1]:
            messages.error(request,err)
        return redirect('login:index')

def login(request):
    results = Userentry.objects.check_user(request.POST)
    if results[0] == True:
		request.session['name'] = results[1].name
		request.session['id'] = results[1].id
		return redirect('appointments:index')
    else:
        for err in results[1]:
            messages.error(request,err)
        return redirect('login:index')

def success(request):
	if not request.session['id']:
		messages.error(request, "You must be logged in first")
		return redirect('login:index')
	messages.success(request, "You have logged in successfully!")
	return render(request, "login/success.html")

def logout(request):
	del request.session['name']
	del request.session['id']
	return redirect('login:index')
