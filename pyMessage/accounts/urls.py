from django.urls import path
from .views import *

urlpatterns = [
    path('register', register),
    path('register/profile_pic', profile_pic),
    path('login', login_view),
    path('logout', logout_view)
]