from django.shortcuts import render
from .models import FriendRequest

# Create your views here.
def requests(request):
    return render(request, 'friend_requests.html')