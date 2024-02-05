import json
from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from .managers import MyUserManager

# Create your models here.

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
        try:
            return UserProfilePic.objects.get(user=self).profile_picture.url
        except:
            return 'static/profile_pictures/default.jpg'
    
    def get_data(self):
        return {
            'name': self.name,
            'username': self.username,
            'picture' : self.profile_picture
        }
                
    def change_info(self, first_name, last_name, email, phone, profile_picture):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        
        user = UserProfilePic.objects.get(user=self)
        user.profile_picture = profile_picture
        user.save()
        
        self.save()
        
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
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='static/profile_pictures/', 
                                        default='static/profile_pictures/default.jpg',
                                        blank=True, null=True)