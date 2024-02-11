from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import MyUserCreationForm, MyUserLoginForm, AddProfilePicForm
from .utils import *
from .models import MyUser

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            login(request, form.instance)
            return redirect('/register/profile_pic')
    else:
        form = MyUserCreationForm()
    return render(request, 'register.html', {'form': form})

def profile_pic(request):
    if request.method == 'POST':
        form = AddProfilePicForm(request.POST, request.FILES)
        form.instance.user = request.user
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = AddProfilePicForm()
        
    return render(request, 'profile_pic.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        field_input = request.POST.get("username")
        password = request.POST.get("password")

        try:
            if is_phone(field_input):
                user = MyUser.objects.get(phone=parse_phone_number(field_input))
            else:
                user = MyUser.objects.get(email=field_input)
        except:
                messages.error(request, "User Not Found....")
                return redirect('/')

        if user is not None and user.check_password(password):
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, "Username or Password does not match...")

    return render(request, 'login.html', {'form': MyUserLoginForm(request, data=request.POST)})

def logout_view(request):
    logout(request)
    return redirect('/login')