from django.db import models
          
MyUser = 'accounts.MyUser'

class Message(models.Model):
    sender = models.ForeignKey(MyUser, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(MyUser, related_name='received_messages', on_delete=models.CASCADE)
    message = models.TextField()
    image = models.ImageField(upload_to='static/message_images/', null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    
    @staticmethod
    def get_messages(user, other):
        return (
            Message.objects.filter(sender=user, receiver=other) | 
            Message.objects.filter(sender=other, receiver=user)
            ).order_by('date')
        
    def get_info(self):
        return {
            'id': self.id,
            'sender': self.sender.id,
            'receiver': self.receiver.id,
            'message': self.message,
            'image': self.image.url if self.image else '',
            'date': str(self.date)
        }
        
        
class Notification(models.Model):
    user_from = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='from_user')
    user_to = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='to_user')
    is_seen = models.BooleanField(default=False)
    
    @staticmethod
    def get_notifications(user, other):
        return Notification.objects.filter(user_from=other, user_to=user, is_seen=False).count()
        
class OnlineStatus(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    online_status = models.BooleanField(default=False)
    
    @staticmethod
    def get_status(user):
        return bool(OnlineStatus.objects.filter(user=user).values_list('online_status', flat=True))