from django.shortcuts import render, redirect
from ..login.models import Userentry
from datetime import date
from .models import Task
from django.core.urlresolvers import reverse
from django.contrib import messages

def index(request):
    try:
        user = request.session['id']
    except:
        messages.error(request, "You must be logged in first")
        return redirect('login:index')
    today = date.today()
    context = {
    "current_date":  today,
    "appointments": Task.objects.filter(owner_id=request.session['id'], date=today).order_by("time"),
    "appointments_future": Task.objects.filter(owner_id=request.session['id'], date__gt=today).order_by("date")
    }
    return render(request, "appointments/index.html", context)

def edit(request, id):
    try:
        user = request.session['id']
    except:
        messages.error(request, "You must be logged in first")
        return redirect('login:index')
    request.session['task'] = id
    context = {
    "tasks": Task.objects.filter(id=id),
    }
    return render (request, 'appointments/edit.html', context)

def destroy(request, id):
    Task.objects.filter(id=id).delete()
    return redirect ('appointments:index')

def add_task(request):
    try:
        user = request.session['id']
    except:
        messages.error(request, "You must be logged in first")
        return redirect('login:index')
    if request.method == 'POST':
        results = Task.objects.add_task(request.POST, request.session)
        if results[0] == True:
    		return redirect('appointments:index')
        else:
            for err in results[1]:
                messages.error(request,err)
            return redirect('appointments:index')
    return redirect ('appointments:index')

def edit_task(request):
    try:
        user = request.session['id']
    except:
        messages.error(request, "You must be logged in first")
        return redirect('login:index')
    print request.POST
    if request.method == 'POST':
        results = Task.objects.edit_task(request.POST, request.session)
        if results[0] == True:
            return redirect('appointments:index')
        else:
            for err in results[1]:
                messages.error(request,err)
                return redirect (reverse('appointments:edit', kwargs={'id':request.session['task']}))
    return redirect ('appointments:index')

def errors(request):
    return render(request, 'books/errors.html')
