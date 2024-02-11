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
        friends_dict[friend.id] = friend.get_data['name']
        try:
            Friends.objects.filter(owner=user).update(friends={friend.id: friend.get_data['name']})
        except:
            Friends.objects.create(owner=user, friends=friends_dict, blocked={})
    
    def add_blocked(user, to_block):
        blocked_dict = Friends.get_blocked(user)
        blocked_dict[to_block.id] = to_block.get_data['name']
        try:
            Friends.objects.filter(owner=user).update(blocked=blocked_dict)
        except:
            Friends.objects.create(owner=user, friends={}, blocked={to_block.id: to_block.get_data['name']})
        
    @staticmethod
    def add_nickname(user, friend, new_name):
        friends_dict = Friends.get_friends(user)
        friends_dict[friend.id] = new_name
        Friends.objects.filter(owner=user).update(friends=friends_dict)
        
    @staticmethod
    def remove_friend(user, friend):
        friends_dict = user.friends
        friends_dict.pop(friend.id)
        Friends.objects.filter(owner=user).update(friends=friends_dict)
    
    @staticmethod
    def remove_blocked(user, to_unblock):
        blocked_dict = Friends.get_blocked(user)
        blocked_dict.pop(to_unblock.id)
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
        sender = request.sender
        receiver = request.receiver
        Friends.add_friend(sender, receiver)
        Friends.add_friend(receiver, sender)
        FriendRequest.objects.get(id=request.id).delete()
        
    @staticmethod
    def decline_request(request):
        FriendRequest.objects.get(id=request.id).delete()
        
    @staticmethod
    def get_requests(user):
        return FriendRequest.objects.filter(receiver=user)
    
    @staticmethod
    def get_sent_requests(user):
        return FriendRequest.objects.filter(sender=user)
    
    @staticmethod
    def remove_request(request):
        FriendRequest.objects.get(id=request.id).delete()
        
    def get_info(self):
        return {
            'id': self.id,
            'sender': self.sender.get_data(),
            'receiver': self.receiver.get_data(),
            'date': self.date
        }