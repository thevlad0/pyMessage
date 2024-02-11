from django.urls import path
from .views import *

urlpatterns = [
    path('search/', search_users),
    path('search/<str:filter_text>/', search_users),
    
    path('friends/requests/', get_friend_requests),
    path('friends/add_friend/<int:friend_id>/', add_friend),
    path('friends/remove_friend/<int:friend_id>/', remove_friend),
    path('friends/add_nickname/<int:friend_id>/<str:new_name>/', add_nickname),
    path('friends/add_blocked/<int:to_block_id>/', add_blocked),
    path('friends/remove_blocked/<int:to_unblock_id>/', remove_blocked),
    path('friends/send_request/<int:to_user_id>/', send_request),
    path('friends/accept_request/<int:from_user_id>/', accept_request),
    path('friends/decline_request/<int:from_user_id>/', decline_request),
]