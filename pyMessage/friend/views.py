from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import FriendRequest
from accounts.models import MyUser

# Create your views here.
@login_required(login_url='/login')
def friend_requests(request):
    return render(request, 'friend_requests.html')

@login_required(login_url='/login')
def blocked_users(request):
    return render(request, 'blocked.html')