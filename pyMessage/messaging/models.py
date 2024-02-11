from django.db import models
from accounts.models import MyUser
          
class Message(models.Model):
    sender = models.ForeignKey(MyUser, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(MyUser, related_name='receieved_messages', on_delete=models.CASCADE)
    message = models.TextField()
    image = models.ImageField(upload_to='static/message_images/', null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    
    @staticmethod
    def get_messages(user, other):
        return (
            Message.objects.filter(sender=user, receiver=other) | 
            Message.objects.filter(sender=other, receiver=user)
            ).order_by('date')
