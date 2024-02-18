import base64
import json
import os
from random import randint
import time
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from pyMessage import settings
from .models import Message, OnlineStatus, Notification
from accounts.models import MyUser
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        my_id = self.scope['user'].id
        other_user_id = self.scope['url_route']['kwargs']['id']
        
        if int(my_id) > int(other_user_id):
            self.room_name = f'{my_id}-{other_user_id}'
        else:
            self.room_name = f'{other_user_id}-{my_id}'

        self.room_group_name = 'chat_%s' % self.room_name
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        if data['type'] == 'message':
            message = data['message']
            user = data['user']
            receiver = data['receiver']
            
            await self.save_message(user, message, receiver)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'user': user,
                }
            )
        else:
            image_data = data['image']
            user = data['user']
            receiver = data['receiver']
            
            format, imgstr = image_data.split(';base64,')
            ext = format.split('/')[-1]

            data = base64.b64decode(imgstr)
            
            file_name = f"received_image{self.scope['user'].id}_{int(time.time())}.{ext}"
            relative_path = os.path.join('uploaded_images', file_name)
            default_storage.save(os.path.join(settings.MEDIA_ROOT, relative_path), ContentFile(data))
            
            await self.save_message(user, 'Image file', receiver, 'uploaded_images/' + file_name)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'image_message',
                    'message': 'media/uploaded_images/' + file_name,
                    'user': user,
                }
            )

    async def chat_message(self, event):
        message = event['message']
        user = event['user']

        await self.send(text_data=json.dumps({
            'message': message,
            'user': user,
            'type': 'message'
        }))
        
    async def image_message(self, event):
        message = event['message']
        user = event['user']

        await self.send(text_data=json.dumps({
            'image': message,
            'message': 'Image file',
            'user': user,
            'type': 'image'
        }))

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    @database_sync_to_async
    def save_message(self, user_data, message, receiver_data, image=None):
        user = MyUser.objects.get(id=user_data)
        receiver = MyUser.objects.get(id=receiver_data)
        chat = Message.objects.create(
            sender=user, message=message, receiver=receiver,
            image=image if image else None)
        other_user_id = self.scope['url_route']['kwargs']['id']
        other = MyUser.objects.get(id=other_user_id)
        if receiver == other:
            Notification.objects.create(user_from=user, user_to=receiver)

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'notify'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
        
    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        user = data['user']
        receiver = data['receiver']
        
        await self.change_notification_status(user, receiver)
        await self.send(json.dumps({
            'user': receiver,
            'count': 0
        }))

    async def disconnect(self, code):
        self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def send_notification(self, event):
        data = json.loads(event.get('value'))
        user = data['user']
        count = data['count']
        await self.send(text_data=json.dumps({
            'user': user,
            'count': count
        }))
        
    @database_sync_to_async
    def change_notification_status(self, user_id, receiver_id):
        print(user_id, receiver_id)
        for notification in Notification.objects.filter(user_from=receiver_id, user_to=user_id, is_seen=False):
            notification.is_seen = True
            notification.save()
        
        
class OnlineStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'user'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):        
        data = json.loads(text_data)
        user = data['user']
        connection_type = data['type']
        await self.change_online_status(user, connection_type)

    async def send_online_status(self, event):
        data = json.loads(event.get('value'))
        user = data['user']
        online_status = data['status']
        await self.send(text_data=json.dumps({
            'user': user,
            'online_status': online_status
        }))


    async def disconnect(self, message):
        self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    @database_sync_to_async
    def change_online_status(self, user_id, c_type):
        userprofile = OnlineStatus.objects.get(user=user_id)
        if c_type == 'online':
            userprofile.online_status = True
            userprofile.save()
        else:
            userprofile.online_status = False
            userprofile.save()