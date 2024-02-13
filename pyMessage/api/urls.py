from django.urls import path
from .views import *

urlpatterns = [
    path('search/', search_users),
    path('search/<str:filter_text>/', search_users),
    
    path('friends/', get_friends),
    
    path('messages/<int:user_id>', get_messages),
    
    path('friends/requests/', get_friend_requests),
    path('friends/get_blocked/', get_blocked_users),
    path('friends/remove_friend/<int:friend_id>/', remove_friend),
    path('friends/add_blocked/<int:to_block_id>/', add_blocked),
    path('friends/remove_blocked/<int:to_unblock_id>/', remove_blocked),
    path('friends/send_request/<int:to_user_id>/', send_request),
    path('friends/accept_request/<int:request_id>/', accept_request),
    path('friends/decline_request/<int:from_user_id>/', decline_request),
]