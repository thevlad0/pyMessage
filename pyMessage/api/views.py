from django.http import JsonResponse
from accounts.models import MyUser

# Create your views here.
def search_users(request, filter_text=None):
    found_users = request.user.search(filter_text)
    return JsonResponse(found_users, safe=False)

def get_friend_requests(request):
    friend_requests = request.user.get_requests()
    sent_requests = request.user.get_sent_requests()
    
    received = [received_request.get_info() for received_request in friend_requests]
    sent = [sent_request.get_info() for sent_request in sent_requests]
    return JsonResponse({'friend_requests': received, 'sent_requests': sent})

def add_friend(request, friend_id):
    friend = MyUser.objects.get(id=friend_id)
    request.user.add_friend(friend)
    
def remove_friend(request, friend_id):
    friend = MyUser.objects.get(id=friend_id)
    request.user.remove_friend(friend)
    
def add_nickname(request, friend_id, new_name):
    friend = MyUser.objects.get(id=friend_id)
    request.user.add_nickname(friend, new_name)
    
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
    current_request = MyUser.objects.get(id=request_id)
    request.user.accept_request(current_request)
    
def decline_request(request, request_id):
    current_request = MyUser.objects.get(id=request_id)
    request.user.decline_request(current_request)