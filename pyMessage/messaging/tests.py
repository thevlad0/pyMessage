from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Message, Notification, OnlineStatus

FIRST_NAME = 'Test'
LAST_NAME = 'User'
EMAIL = 'test@gmail.com'
PHONE1 = '0881122345'
PHONE2 = '+359881122345'
PASSWORD = 'testpassword'

# Create your tests here.
class MessageModelTest(TestCase):
    def setUp(self):
        self.user1 = get_user_model().objects.create(
            first_name=FIRST_NAME,
            last_name=LAST_NAME,
            email=EMAIL,
            phone=PHONE2,
            password=PASSWORD
        )
        OnlineStatus.objects.create(user=self.user1)
        
        self.user2 = get_user_model().objects.create(
            first_name=FIRST_NAME + '2',
            last_name=LAST_NAME + '2',
            email='test2@gmail.com',
            phone='0881122356',
            password=PASSWORD
        )
        OnlineStatus.objects.create(user=self.user2)

    def test_get_messages(self):
        message1 = Message.objects.create(
            sender=self.user1, 
            receiver=self.user2, 
            message='Test message 1'
            )
        message2 = Message.objects.create(
            sender=self.user1, 
            receiver=self.user2, 
            message='Test message 2'
            )

        messages = Message.get_messages(self.user1, self.user2)

        self.assertEqual(len(messages), 2)
        self.assertIn(message1, messages)
        self.assertIn(message2, messages)

    def test_get_info(self):
        message = Message.objects.create(
            sender=self.user1, 
            receiver=self.user2, 
            message='Test message'
            )

        info = message.get_info()

        self.assertEqual(info['id'], message.id)
        self.assertEqual(info['sender'], self.user1.id)
        self.assertEqual(info['receiver'], self.user2.id)
        self.assertEqual(info['message'], 'Test message')
        self.assertEqual(info['image'], '')
        self.assertEqual(info['date'], str(message.date))
        
    def test_notifications_count(self):
        message = Message.objects.create(
            sender=self.user1, 
            receiver=self.user2, 
            message='Test message'
            )

        notification = Notification.objects.create(
            user_from=self.user1, 
            user_to=self.user2
            )

        count = Notification.get_notifications(self.user2, self.user1)

        self.assertEqual(count, 1)
        
    def test_online_status(self):
        status1 = OnlineStatus.get_status(self.user1)
        self.assertEqual(status1, False)
        
        status2 = OnlineStatus.get_status(self.user2)
        self.assertEqual(status2, False)