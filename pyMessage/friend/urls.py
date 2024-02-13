from django.urls import path
from .views import *

urlpatterns = [
    path('requests', friend_requests),
    path('blocked', blocked_users)
]