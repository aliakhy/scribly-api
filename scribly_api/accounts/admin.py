from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# from django.contrib.auth.admin import UserAdmin
from .models import User
# Register your models here.
# admin.site.register(User)



@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ('id','username','email','is_staff','is_superuser','is_active')
    search_fields = ['username', ]
    list_filter = ['is_staff', 'is_superuser', 'is_active']
    ordering = ['id']
    readonly_fields = ('date_joined', 'last_login')

    fieldsets = [
        (
        'info',{
            'fields': ('username','email','password','about_me','is_staff','is_superuser','is_active','avatar','groups', 'user_permissions'),
        }
        ),
        (
        'date',{
            'fields': ('last_login', 'date_joined'),
        }
        )
    ]
