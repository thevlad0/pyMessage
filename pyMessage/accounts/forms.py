from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django import forms
from phonenumber_field.formfields import PhoneNumberField
from .models import MyUser

class MyUserCreationForm(UserCreationForm):
    first_name = forms.CharField(label=('First Name:'), max_length=25, required=True,
                                 widget=forms.TextInput(attrs={'class': 'textBox',
                                                               'autofocus': True,}))
    last_name = forms.CharField(label=('Last Name:'), max_length=25, required=True, 
                                widget=forms.TextInput(attrs={'class': 'textBox',}))
    phone = PhoneNumberField(label=('Phone:'), region='BG', required=True,
                             widget=forms.TextInput(attrs={'class': 'textBox',}))
    email = forms.EmailField(label=('Email:'), max_length=50, required=False,
                             widget=forms.EmailInput(attrs={'class': 'textBox'}))
    password1 = forms.CharField(label=('Password:'), max_length=30, required=True, 
                                widget=forms.PasswordInput(attrs={'class': 'textBox'}))
    password2 = forms.CharField(label=('Confirm password:'), max_length=30, required=True, 
                                widget=forms.PasswordInput(attrs={'class': 'textBox'}))
    
    class Meta:
        model = MyUser
        fields = ('first_name', 'last_name', 'phone', 'email', 'password1', 'password2')

class MyUserChangeForm(UserChangeForm):
        
    class Meta:
        model = MyUser
        fields = ('first_name', 'last_name', 'phone', 'email')

class MyUserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Phone/Email:', max_length=50, required=True,
                               widget=forms.TextInput(attrs={'class': 'textBox',
                                                             'placeholder': 'Phone/Email',
                                                             'autofocus': True
                                                             }))
    password = forms.CharField(label='Password:', max_length=30, required=True,
                               widget=forms.PasswordInput(attrs={'class': 'textBox',
                                                                 'placeholder': 'Password',
                                                                }))