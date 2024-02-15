from django.db import models

MyUser = 'accounts.MyUser'

# Create your models here.
class Friends(models.Model):
    owner = models.ForeignKey(MyUser, related_name='friends', on_delete=models.CASCADE)
    friends = models.JSONField()
    blocked = models.JSONField()
    
    @staticmethod
    def get_friends(user):
        try:
            friends = Friends.objects.get(owner=user).friends
            return friends
        except:
            return {}
        
    def get_blocked(user):
        try:
            blocked = Friends.objects.get(owner=user).blocked
            return blocked
        except:
            return {}
    
    @staticmethod
    def add_friend(user, friend):
        friends_dict = Friends.get_friends(user)
        friends_dict[friend.id] = friend.get_data()['name']
    
        found = Friends.objects.filter(owner=user).update(friends=friends_dict)
        if not found:
            Friends.objects.create(owner=user, friends=friends_dict, blocked={})
            
    def add_blocked(user, to_block):
        blocked_dict = Friends.get_blocked(user)
        blocked_dict[to_block.id] = to_block.get_data()['name']
        
        found = Friends.objects.filter(owner=user).update(blocked=blocked_dict)
        if not found:
            Friends.objects.create(owner=user, friends={}, blocked=blocked_dict)
        
    @staticmethod
    def remove_friend(user, friend):
        friends_dict = user.friends
        friends_dict.pop(str(friend.id))
        Friends.objects.filter(owner=user).update(friends=friends_dict)
    
    @staticmethod
    def remove_blocked(user, to_unblock):
        blocked_dict = Friends.get_blocked(user)
        blocked_dict.pop(str(to_unblock.id))
        Friends.objects.filter(owner=user).update(blocked=blocked_dict)
        

class FriendRequest(models.Model):
    sender = models.ForeignKey(MyUser, related_name='sent_requests', on_delete=models.CASCADE)
    receiver = models.ForeignKey(MyUser, related_name='received_requests', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    
    @staticmethod
    def send_request(sender, receiver):
        FriendRequest.objects.create(sender=sender, receiver=receiver)
        
    @staticmethod
    def accept_request(request):
        request_info = FriendRequest.objects.get(id=request)
        Friends.add_friend(request_info.sender, request_info.receiver)
        Friends.add_friend(request_info.receiver, request_info.sender)
        FriendRequest.objects.get(id=request).delete()
        return request_info
        
    @staticmethod
    def decline_request(request):
        FriendRequest.objects.get(id=request).delete()
        
    @staticmethod
    def get_requests(user):
        return FriendRequest.objects.filter(receiver=user).values_list('id', flat=True)
    
    @staticmethod
    def get_sent_requests(user):
        return FriendRequest.objects.filter(sender=user).values_list('id', flat=True)
        
    def get_info(self):
        return {
            'id': self.id,
            'sender': self.sender.get_data(),
            'receiver': self.receiver.get_data(),
            'date': str(self.date)
        }