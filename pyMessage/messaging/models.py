from django.db import models
from accounts.models import MyUser

class Friends(models.Model):
    owner = models.ForeignKey(MyUser, related_name='friends', on_delete=models.CASCADE)
    friends = models.JSONField()
    
    @staticmethod
    def add_friend(user, friend):
        friends_dict = user.friends
        friends_dict[friend.id] = friend.get_data['name']
        user.save()
        
    @staticmethod
    def change_friend_name(user, friend, new_name):
        friends_dict = user.friends
        friends_dict[friend.id] = new_name
        user.save()
        
    @staticmethod
    def remove_friend(user, friend):
        friends_dict = user.friends
        friends_dict.pop(friend.id)
        user.save()
        
        
class Message(models.Model):
    sender = models.ForeignKey(MyUser, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(MyUser, related_name='receieved_messages', on_delete=models.CASCADE)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    
    @staticmethod
    def get_messages(user, other):
        return (
            Message.objects.filter(sender=user, receiver=other) | 
            Message.objects.filter(sender=other, receiver=user)
            ).order_by('date')
