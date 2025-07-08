from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden

from .models import Task
from .forms import TaskForm

# 🔐 User Registration View
def register_view(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    return render(request, 'register.html', {'form': form})

# 🔐 User Login View
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
    return render(request, 'login.html')

# 🔐 User Logout View
def logout_view(request):
    logout(request)
    return redirect('login')

# 🏠 Dashboard View
@login_required
def home(request):
    # Handle task creation
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('home')
    else:
        form = TaskForm()

    # Display based on user role
    if request.user.is_superuser:
        users = User.objects.all()
        tasks = Task.objects.select_related('user')
        return render(request, 'home.html', {
            'users': users,
            'tasks': tasks,
            'admin': True,
            'form': form
        })
    else:
        tasks = Task.objects.filter(user=request.user)
        return render(request, 'home.html', {
            'tasks': tasks,
            'admin': False,
            'form': form
        })

# ✅ Toggle Task Complete/Incomplete
@login_required
def toggle_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if task.user != request.user and not request.user.is_superuser:
        return HttpResponseForbidden()
    task.completed = not task.completed
    task.save()
    return redirect('home')

# ❌ Delete Task
@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if task.user != request.user and not request.user.is_superuser:
        return HttpResponseForbidden()
    task.delete()
    return redirect('home')