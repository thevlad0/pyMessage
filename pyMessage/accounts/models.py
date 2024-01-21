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
    
    def __str__(self):
        return str(self.phone)