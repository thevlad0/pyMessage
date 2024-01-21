from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import MyUserCreationForm, MyUserChangeForm
from .models import MyUser

# Register your models here.

class MyAdmin(UserAdmin):
    add_form = MyUserCreationForm
    form = MyUserChangeForm

    model = MyUser

    list_display = ('phone', 'email', 'is_active',
                    'is_staff', 'is_superuser', 'last_login',)
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('phone', 'email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active',
         'is_superuser', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )
    exclude = ('username',)
    
    search_fields = ('email', 'phone')
    ordering = ('email', 'phone')

admin.site.register(MyUser, MyAdmin)