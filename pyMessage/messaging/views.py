from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.models import MyUser
from .models import Friends

# Create your views here.
@login_required(login_url='/login')
def main_view(request):
    friends = Friends.get_friends(request.user)
    friend_data = [MyUser.objects.get(id=id).get_data() for id in friends.keys()]
    return render(request, 'index.html', {'friends': friend_data, 'user': request.user.get_data()})