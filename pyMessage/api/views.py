from django.http import JsonResponse
from accounts.models import MyUser
from messaging.models import Message
import json

# Create your views here.
def get_friends(request):
    friend_data = request.user.get_friends()
    friends = json.dumps([
        MyUser.objects.get(id=friend).get_data() for friend in friend_data
    ])
    return JsonResponse(friends, safe=False)

def search_users(request, filter_text=None):
    found_users = request.user.search(filter_text)
    users = json.dumps([
        MyUser.objects.get(id=user).get_data() for user in found_users
    ])
    return JsonResponse(users, safe=False)

def get_blocked_users(request):
    blocked_data = request.user.get_blocked()
    blocked = json.dumps([
        MyUser.objects.get(id=blocked).get_data() for blocked in blocked_data
    ])
    return JsonResponse(blocked, safe=False)

def get_messages(request, user_id):
    messages_data = request.user.get_messages(user_id)
    messages = json.dumps([
        Message.objects.get(id=message_id) for message_id in messages_data
    ])
    return JsonResponse(messages, safe=False)

def get_friend_requests(request):
    friend_requests = request.user.get_requests()
    requests = json.dumps([
        MyUser.objects.get(id=request).get_data() for request in friend_requests
    ])
    return JsonResponse(requests, safe=False)
    
def remove_friend(request, friend_id):
    friend = MyUser.objects.get(id=friend_id)
    request.user.remove_friend(friend)
    
def add_blocked(request, to_block_id):
    to_block = MyUser.objects.get(id=to_block_id)
    request.user.add_blocked(to_block)
    
def remove_blocked(request, to_unblock_id):
    to_unblock = MyUser.objects.get(id=to_unblock_id)
    request.user.remove_blocked(to_unblock)
    
def send_request(request, to_user_id):
    to_user = MyUser.objects.get(id=to_user_id)
    request.user.send_request(to_user)
    
def accept_request(request, request_id):
    request.user.accept_request(request_id)
    
def decline_request(request, request_id):
    request.user.decline_request(request_id)