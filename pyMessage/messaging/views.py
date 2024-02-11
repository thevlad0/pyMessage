from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='/login')
def main_view(request):
    friends = request.user.get_friends()
    #friend_data = [MyUser.objects.get(id=id).get_data() for id in friends.keys()]
    friend_data = [friend.get_data() for friend in friends]
    return render(request, 'index.html', {'friends': friend_data, 'user': request.user.get_data()})