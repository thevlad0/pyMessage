from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from accounts.models import MyUser

# Create your views here.
@login_required(login_url='/login')
def main_view(request):
    return render(request, 'index.html', {'user': request.user.get_data()})