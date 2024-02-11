import json
from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from .managers import MyUserManager
from friend.models import Friends, FriendRequest

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
            'name': self.name,
            'username': self.username,
            'picture' : self.profile_picture,
        }
                
    def change_info(self, first_name, last_name, email, phone, profile_picture):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        
        UserProfilePic.objects.filter(user=self).update(profile_picture=profile_picture)
        
        self.save()
        
    def get_friends(self):
        return Friends.get_friends(self)
    
    def get_blocked(self):
        return Friends.get_blocked(self)
    
    def add_friend(self, friend):
        Friends.add_friend(self, friend)
        
    def add_blocked(self, to_block):    
        Friends.add_blocked(self, to_block)
        
    def add_nickname(self, friend, new_name):
        Friends.add_nickname(self, friend, new_name)
        
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
        FriendRequest.decline_request(self, request)
        
    def search(self, filter_text):
        if filter_text is None:
            return json.dumps([user.get_data() for user in MyUser.objects.all()])
        else:
            users = MyUser.objects.filter(
                models.Q(first_name__icontains=filter_text) |
                models.Q(last_name__icontains=filter_text) |
                models.Q(phone__icontains=filter_text) |
                models.Q(email__icontains=filter_text)
            )
        
        return json.dumps([user.get_data() for user in users])   
    
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