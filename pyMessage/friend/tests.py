from django.test import TestCase
from django.contrib.auth import get_user_model
from messaging.models import OnlineStatus
from .models import FriendRequest

FIRST_NAME = 'Test'
LAST_NAME = 'User'
EMAIL = 'test@gmail.com'
PHONE1 = '0881122345'
PHONE2 = '+359881122345'
PASSWORD = 'testpassword'

# Create your tests here.
class FriendTestCase(TestCase):
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
        
        self.user3 = get_user_model().objects.create(
            first_name=FIRST_NAME + '3',
            last_name=LAST_NAME + '3',
            email='test3@gmail.com',
            phone='0881122357',
            password=PASSWORD
        )
        OnlineStatus.objects.create(user=self.user3)
        
    def test_add_friend(self):
        user2_repr = {
            str(self.user2.id): self.user2.first_name + ' ' + self.user2.last_name
        }
        user3_repr = {
            str(self.user3.id): self.user3.first_name + ' ' + self.user3.last_name
        }
        
        self.user1.add_friend(self.user2)
        self.assertEqual(self.user1.get_friends(), user2_repr)
        
        self.user1.add_friend(self.user3)
        self.assertEqual(self.user1.get_friends(), user2_repr | user3_repr)
        
        self.user1.remove_friend(self.user2)
        self.assertEqual(self.user1.get_friends(), user3_repr)
        
    def test_block_user(self):
        user2_repr = {
            str(self.user2.id): self.user2.first_name + ' ' + self.user2.last_name
        }
        user3_repr = {
            str(self.user3.id): self.user3.first_name + ' ' + self.user3.last_name
        }
        
        self.user1.add_blocked(self.user2)
        self.assertEqual(self.user1.get_blocked(), user2_repr)
        self.assertEqual(self.user2.get_blocked(), {})
        
        self.user1.add_blocked(self.user3)
        self.assertEqual(self.user1.get_blocked(), user2_repr | user3_repr)
        
        self.user1.remove_blocked(self.user2)
        self.assertEqual(self.user1.get_blocked(), user3_repr)
        
        
class FriendRequestTestCase(TestCase):
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
        
    def test_send_request(self):
        self.user1.send_request(self.user2)
        
        request = FriendRequest.objects.get(sender=self.user1, receiver=self.user2)
        
        self.assertEqual(list(self.user2.get_requests()), [request.id])
        self.assertEqual(list(self.user1.get_sent_requests()), [request.id])
        self.assertEqual(list(self.user1.get_requests()), [])
        self.assertEqual(list(self.user2.get_sent_requests()), [])
        
    def test_accept_request(self):
        self.user1.send_request(self.user2)
        
        request = FriendRequest.objects.get(sender=self.user1, receiver=self.user2)
        
        self.user2.accept_request(request.id)
        
        self.assertEqual(list(self.user1.get_friends()), [str(self.user2.id)])
        self.assertEqual(list(self.user2.get_friends()), [str(self.user1.id)])
        self.assertEqual(list(self.user2.get_requests()), [])
        self.assertEqual(list(self.user1.get_sent_requests()), [])
        
    def test_decline_request(self):
        self.user1.send_request(self.user2)
        
        request = FriendRequest.objects.get(sender=self.user1, receiver=self.user2)
        
        self.user2.decline_request(request.id)
        
        self.assertEqual(list(self.user2.get_requests()), [])
        self.assertEqual(list(self.user1.get_sent_requests()), [])