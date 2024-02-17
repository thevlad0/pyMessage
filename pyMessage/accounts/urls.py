from django.urls import path
from .views import *

urlpatterns = [
    path('register', register, name='register'),
    path('register/profile_pic', profile_pic, name='profile_pic'),
    path('profile/edit', edit, name='edit'),
    path('login', login_view, name='login'),
    path('logout', logout_view, name='logout')
]