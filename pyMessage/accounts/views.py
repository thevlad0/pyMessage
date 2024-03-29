from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import MyUserCreationForm, MyUserLoginForm, AddProfilePicForm
from .utils import *
from .models import MyUser, UserProfilePic
from messaging.models import OnlineStatus

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            OnlineStatus.objects.create(user=form.instance)
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

@login_required(login_url='/login')
def edit(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        
        form = AddProfilePicForm(request.POST, request.FILES)
        form.instance.user = request.user
        if form.is_valid():
            UserProfilePic.objects.filter(user=request.user).delete()
            request.user.change_info(first_name, last_name, email, phone)
            form.save()
            return redirect('/')
        
    form = AddProfilePicForm()
    return render(request, 'edit.html', {'form': form})

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