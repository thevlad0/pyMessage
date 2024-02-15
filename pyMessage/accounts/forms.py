from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django import forms
from phonenumber_field.formfields import PhoneNumberField
from .models import MyUser, UserProfilePic

class MyUserCreationForm(UserCreationForm):
    first_name = forms.CharField(label=('First Name:'), max_length=25, required=True,
                                 widget=forms.TextInput(attrs={'class': 'w-full px-3 py-1.5 border border-gray-400 rounded-lg focus:outline-none focus:border-blue-500',
                                                               'placeholder': 'First name',
                                                               'autofocus': True,}))
    last_name = forms.CharField(label=('Last Name:'), max_length=25, required=True, 
                                widget=forms.TextInput(attrs={'class': 'w-full px-3 py-1.5 border border-gray-400 rounded-lg focus:outline-none focus:border-blue-500',
                                                              'placeholder': 'Last name',
                                                              }))
    phone = PhoneNumberField(label=('Phone:'), region='BG', required=True,
                             widget=forms.TextInput(attrs={'class': 'w-full px-3 py-1.5 border border-gray-400 rounded-lg focus:outline-none focus:border-blue-500',
                                                           'placeholder': 'Phone number',
                                                           }))
    email = forms.EmailField(label=('Email:'), max_length=50, required=False,
                             widget=forms.EmailInput(attrs={'class': 'w-full px-3 py-1.5 border border-gray-400 rounded-lg focus:outline-none focus:border-blue-500',
                                                            'placeholder': 'Email',
                                                            }))
    password1 = forms.CharField(label=('Password:'), max_length=30, required=True, 
                                widget=forms.PasswordInput(attrs={'class': 'w-full px-3 py-1.5 border border-gray-400 rounded-lg focus:outline-none focus:border-blue-500',
                                                                  'placeholder': 'Password',
                                                                  }))
    password2 = forms.CharField(label=('Confirm password:'), max_length=30, required=True, 
                                widget=forms.PasswordInput(attrs={'class': 'w-full px-3 py-1.5 border border-gray-400 rounded-lg focus:outline-none focus:border-blue-500',
                                                                  'placeholder': 'Confirm password',
                                                                  }))
    
    class Meta:
        model = MyUser
        fields = ('first_name', 'last_name', 'phone', 'email', 'password1', 'password2')


class MyUserChangeForm(UserChangeForm):
    class Meta:
        model = MyUser
        fields = ('first_name', 'last_name', 'phone', 'email')


class MyUserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Phone/Email:', max_length=50, required=True,
                               widget=forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-400 rounded-lg focus:outline-none focus:border-blue-500',
                                                             'placeholder': 'Phone/Email',
                                                             'autofocus': True
                                                             }))
    password = forms.CharField(label='Password:', max_length=30, required=True,
                               widget=forms.PasswordInput(attrs={'class': 'w-full px-3 py-2 border border-gray-400 rounded-lg focus:outline-none focus:border-blue-500',
                                                                 'placeholder': 'Password',
                                                                }))
    
    
class AddProfilePicForm(forms.ModelForm):
    profile_picture = forms.ImageField(label=('Profile Picture:'), 
                                       required=False, 
                                       widget=forms.FileInput(attrs={
                                           'class': 'w-full border border-black-300 rounded-md px-3 py-2 focus:outline-none focus:border-blue-500'
                                       }))
    
    class Meta:
        model = UserProfilePic
        fields = ('profile_picture',)
        widgets = {'user': forms.HiddenInput()}