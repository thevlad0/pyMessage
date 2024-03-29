from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import OnlineStatus, Notification 
import json

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@receiver(post_save, sender=Notification)
def send_notification(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        notification_obj = Notification.objects.filter(is_seen=False, user_to=instance.user_to, user_from=instance.user_from).count()
        user = str(instance.user_from.id)
        print(user, notification_obj)
        data = {
            'user': user,
            'count': notification_obj,
        }

        async_to_sync(channel_layer.group_send)(
            'notify', {
                'type': 'send_notification',
                'value': json.dumps(data)
            }
        )


@receiver(post_save, sender=OnlineStatus)
def send_online_status(sender, instance, created, **kwargs):
    if not created:
        channel_layer = get_channel_layer()
        user = instance.user.id
        user_status = instance.online_status

        data = {
            'user': user,
            'status': user_status
        }
        
        async_to_sync(channel_layer.group_send)(
            'user', {
                'type': 'send_online_status',
                'value': json.dumps(data)
            }
        )