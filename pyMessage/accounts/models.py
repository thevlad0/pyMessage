from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from .managers import MyUserManager

# Create your models here.

class MyUser(AbstractUser):
    username = None
    phone = PhoneNumberField(('phone'), region='BG', unique=True)
    email = models.EmailField(('email address'), unique=True)
    
    profile_picture = models.ImageField(upload_to='profile_pictures/', default='profile_pictures/default.png')

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ('first_name', 'last_name', 'password')

    objects = MyUserManager()
    
    def get_data(self):
        return {
            'name': self.first_name + ' ' + self.last_name,
            'username': self.phone if self.phone is not None else self.email,
            'picture' : self.profile_picture.url
        }
    
    def __str__(self):
        return str(self.phone)