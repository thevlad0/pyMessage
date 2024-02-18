from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import UserProfilePic
from messaging.models import OnlineStatus
from .views import *

# Create your tests here.

FIRST_NAME = 'Test'
LAST_NAME = 'User'
EMAIL = 'test@gmail.com'
PHONE1 = '0881122345'
PHONE2 = '+359881122345'
PASSWORD = 'testpassword'

class RegistrationTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')
        self.profile_pic_url = reverse('profile_pic')
    
    def test_user_registration(self):        
        response = self.client.post(self.register_url, {
            'first_name': FIRST_NAME,
            'last_name': LAST_NAME,
            'email': EMAIL,
            'phone': PHONE1,
            'password1': PASSWORD,
            'password2': PASSWORD,
        })
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.profile_pic_url)
        
        self.assertEqual(get_user_model().objects.count(), 1)
        self.assertEqual(get_user_model().objects.first().phone, PHONE2)
        
        self.assertEqual(OnlineStatus.objects.count(), 1)
        self.assertEqual(OnlineStatus.objects.first().user, 
                         get_user_model().objects.first())
        
    def test_profile_pic(self):
        user = get_user_model().objects.create(
            first_name=FIRST_NAME,
            last_name=LAST_NAME,
            email=EMAIL,
            phone=PHONE2,
            password=PASSWORD
        )
        
        self.client.force_login(user)
        response = self.client.post(self.profile_pic_url, {
            'profile_picture': 'test.jpg'
        })
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')
        
        self.assertEqual(UserProfilePic.objects.count(), 1)
        self.assertEqual(UserProfilePic.objects.first().user, user)


class LoginTestCase(TestCase):       
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')
        self.user = get_user_model().objects.create(
            first_name=FIRST_NAME,
            last_name=LAST_NAME,
            email=EMAIL,
            phone=PHONE2,
            password=PASSWORD
        )
    
    def test_user_login(self):
        response1 = self.client.post(self.login_url, {
            'username': PHONE1,
            'password': PASSWORD,
        })
        
        self.assertEqual(response1.status_code, 200)
        
        response2 = self.client.post(self.login_url, {
            'username': PHONE2,
            'password': PASSWORD,
        })
        
        self.assertEqual(response2.status_code, 200)
        
        response3 = self.client.post(self.login_url, {
            'username': EMAIL,
            'password': PASSWORD,
        })
        
        self.assertEqual(response3.status_code, 200)
        
        response4 = self.client.post(self.login_url, {
            'username': 'WRONG@gmail.com',
            'password': PASSWORD,
        })
        
        self.assertNotEqual(response4.status_code, 200)
        
class EditTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.edit_url = reverse('edit')
        self.user = get_user_model().objects.create(
            first_name=FIRST_NAME,
            last_name=LAST_NAME,
            email=EMAIL,
            phone=PHONE2,
            password=PASSWORD
        )
        OnlineStatus.objects.create(user=self.user)
        
    def test_no_changes(self):
        self.client.force_login(self.user)
        response = self.client.post(self.edit_url, {
            'first_name': '',
            'last_name': '',
            'email': '',
            'phone': '',
        })
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')
        
        user = get_user_model().objects.first()
        self.assertEqual(user.first_name, FIRST_NAME)
        self.assertEqual(user.last_name, LAST_NAME)
        self.assertEqual(user.email, EMAIL)
        self.assertEqual(user.phone, PHONE2)
        
    def test_changes(self):
        self.client.force_login(self.user)
        response = self.client.post(self.edit_url, {
            'first_name': '',
            'last_name': 'Name',
            'email': 'newEmail@gmail.com',
            'phone': '',
        })
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')
        
        user = get_user_model().objects.first()
        self.assertEqual(user.first_name, FIRST_NAME)
        self.assertEqual(user.last_name, 'Name')
        self.assertEqual(user.email, 'newEmail@gmail.com')
        self.assertEqual(user.phone, PHONE2)
        
class SearchTestCase(TestCase):
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
        
    def test_search(self):
        self.assertEqual(self.user1.search(FIRST_NAME), [self.user2.id, self.user3.id])
        self.assertEqual(self.user1.search(FIRST_NAME + '2'), [self.user2.id])
        self.assertEqual(self.user1.search(FIRST_NAME + '23'), [])
        self.assertEqual(self.user1.search(''), [self.user2.id, self.user3.id])
        
    def test_search_friends(self):
        self.user1.add_friend(self.user3)
        
        self.assertEqual(self.user1.search(FIRST_NAME), [self.user2.id])
        self.assertEqual(self.user1.search(FIRST_NAME + '2'), [self.user2.id])
        self.assertEqual(self.user1.search(FIRST_NAME + '3'), [])
        
    def test_search_blocked(self):
        self.user1.add_blocked(self.user2)
        
        self.assertEqual(self.user1.search(FIRST_NAME), [self.user3.id])
        self.assertEqual(self.user1.search(FIRST_NAME + '2'), [])
        self.assertEqual(self.user1.search(FIRST_NAME + '3'), [self.user3.id])
        
    def test_search_friends_blocked(self):
        self.user1.add_friend(self.user2)
        self.user1.add_blocked(self.user3)
        
        self.assertEqual(self.user1.search(FIRST_NAME + '2'), [])
        self.assertEqual(self.user1.search(FIRST_NAME + '3'), [])