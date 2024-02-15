from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from .managers import MyUserManager
from friend.models import Friends, FriendRequest
from messaging.models import Message, OnlineStatus

# Create your models here.
DEFAULT_PROFILE_PIC = 'profile_pictures/default.jpg'

class MyUser(AbstractUser):
    username = None
    phone = PhoneNumberField(('phone'), region='BG', unique=True)
    email = models.EmailField(('email address'), unique=True)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ('first_name', 'last_name', 'password')

    objects = MyUserManager()
    
    @property
    def name(self):
        return self.first_name + ' ' + self.last_name
    
    @property
    def username(self):
        return str(self.phone) if self.phone is not None else str(self.email)
    
    @property
    def profile_picture(self):
        return UserProfilePic.get_profile_pic(self)
    
    def get_data(self):
        return {
            'id': self.id,
            'name': self.name,
            'username': self.username,
            'phone': str(self.phone),
            'email': self.email if self.email is not None else '',
            'picture' : self.profile_picture,
            'status': 'online' if int(OnlineStatus.objects.filter(user=self)
            .values_list('online_status', flat=True)[0]) else 'offline'
        }
                
    def change_info(self, first_name, last_name, email, phone):
        MyUser.objects.filter(id=self.id).update(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone
        )
        
    def get_friends(self):
        return Friends.get_friends(self)
    
    def get_blocked(self):
        return Friends.get_blocked(self)
    
    def add_friend(self, friend):
        Friends.add_friend(self, friend)
        
    def add_blocked(self, to_block):    
        Friends.add_blocked(self, to_block)
        
    def remove_friend(self, friend):
        Friends.remove_friend(self, friend)
        
    def remove_blocked(self, to_unblock):
        Friends.remove_blocked(self, to_unblock)
        
    def get_requests(self):
        return FriendRequest.get_requests(self)
    
    def get_sent_requests(self):
        return FriendRequest.get_sent_requests(self)
    
    def send_request(self, to_user):
        FriendRequest.send_request(self, to_user)
        
    def accept_request(self, request):
        FriendRequest.accept_request(request)
        
    def decline_request(self, request):
        FriendRequest.decline_request(request)
        
    def search(self, filter_text):
        users = MyUser.objects.filter(
            models.Q(first_name__icontains=filter_text) |
            models.Q(last_name__icontains=filter_text) |
            models.Q(phone__icontains=filter_text)
        ).values_list('id', flat=True)
        
        got_requests = self.get_requests().values_list('sender')
        sent_requests = self.get_sent_requests().values_list('receiver')
        friends = self.get_friends()
        blocked = self.get_blocked()
        
        return [user for user in users 
                if str(user) not in got_requests
                and str(user) not in sent_requests
                and str(user) not in friends 
                and str(user) not in blocked
                and str(user) != str(self.id)]
    
    def get_messages(self, other):
        return Message.get_messages(self, other).values_list('id', flat=True)
    
    def __str__(self):
        return str(self.phone)
    

class UserProfilePic(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', 
                                        default=DEFAULT_PROFILE_PIC,
                                        blank=False, null=False)
    
    @staticmethod
    def get_profile_pic(user):
        try:
            return UserProfilePic.objects.get(user=user).profile_picture.url
        except:
            return DEFAULT_PROFILE_PIC