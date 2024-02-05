from django.urls import path
from .views import *

urlpatterns = [
    path('search/', search_users),
    path('search/<str:filter_text>/', search_users),
]