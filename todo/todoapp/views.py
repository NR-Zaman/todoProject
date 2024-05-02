from django.http import HttpResponseRedirect
from urllib.parse import urlparse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, login as customlogin
from django.contrib import messages

from .forms import taskForm
from .models import task
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'todoapp/index.html',{})


def register(request):
    if request.user.is_authenticated:
        return redirect('home-page')
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if len(password) < 3:
            messages.error(request, 'Password must be at least 3 characters')
            return redirect('register')

        get_all_users_by_username = User.objects.filter(username=username)
        if get_all_users_by_username:
            messages.error(request, 'Error, username already exists, User another.')
            return redirect('register')

        new_user = User.objects.create_user( username=username, email=email, password=password)
        new_user.is_active = False
        new_user.firstname = firstname
        new_user.lastname = lastname
        new_user.save()
        messages.success(request, 'User successfully created, login now')
        return redirect('/login')
    return render(request, 'todoapp/register.html', {})

def logoutview(request):
    logout(request)
    return redirect('login')


def login(request):
    if request.user.is_authenticated:
        return redirect('home-page')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        validate_user = authenticate(username=username, password=password)
        if validate_user is not None:
            customlogin(request, validate_user)
            return redirect('/')
        else:
            messages.error(request, 'Error, wrong user details or user does not exist')
            return redirect('login')
    return render(request, 'todoapp/login.html', {})


def createtask(request):
    if request.method == 'POST':
        taskname = request.POST.get('taskname')
        dadeline = request.POST.get('dadeline')
        status = request.POST.get('status')
        details = request.POST.get('details')
        comment = request.POST.get('comment')
        new_task = task(user=request.user, taskname=taskname, dadeline=dadeline, status=status, details=details, comment=comment)
        new_task.save()

    all_task = task.objects.filter(user=request.user)
    context = {
        'task': all_task
    }
    return render(request, 'todoapp/create-task.html', context)


def tasklist(request):
    all_task = task.objects.filter(user=request.user)
    context = {
        'task': all_task
    }
    return render(request, 'todoapp/task-list.html', context)


# @login_required
# def update(request, name):
#     get_task = task.objects.get(user=request.user, taskname=name)
#     get_task.status = True
#     get_task.save()
#     return redirect(request, 'todoapp/update-task.html')
#

@login_required
def deletetask(request, name):
    get_task = task.objects.get(user=request.user, taskname=name)
    get_task.delete()
    return redirect('home-page')


@login_required
def detailsview(request, name):
    all_task = task.objects.filter(user=request.user)
    context = {
        'task': all_task
    }
    return redirect('details.html',context)


def edit(request, id):
    get_task = task.objects.get(id=id)
    get_task.status = True
    get_task.save()
    return render(request, 'todoapp/update-task.html', {'get-task': get_task})


def update(request, id):
    new_task = task.objects.get(id=id)
    form = taskForm(request.POST, instance=new_task)
    if form.is_valid():
        form.save()
        return redirect("tasklist")
    return render(request, 'todoapp/task-list.html', {'new_task': new_task})


def detailsview(request, id):
    get_task = task.objects.get(id=id)
    get_task.status = True
    get_task.save()
    return render(request, 'todoapp/details.html', {'get-task': get_task})
