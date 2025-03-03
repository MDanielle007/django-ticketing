from django.shortcuts import render, redirect
from .forms import RegisterForm  # You'll need to create a register form
from django.contrib.auth import login
from .models import User

# Create your views here.
def index(request):
    return render(request, 'users/index.html')  

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Redirect to the home page or dashboard
    else:
        form = RegisterForm()
    return render(request, 'auth_app/register.html', {'form': form})

from django.contrib.auth import authenticate, login

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'auth_app/login.html', {'error': 'Invalid login credentials'})
    return render(request, 'auth_app/login.html')

from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('auth_app:login')