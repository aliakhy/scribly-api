from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

def user_avatar_path(instance, filename):
    return f'users/{instance.id}/{filename}'
# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not username:
            raise ValueError('Users must have an username')
        if not email:
            raise ValueError('Users must have an email')
        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, username, email, password=None):
        user = self.create_user(username, email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        max_length=25,
        unique=True,
    )
    email = models.EmailField(
        max_length=25,
        unique=True,
    )
    is_active = models.BooleanField(
        default=True,
    )
    about_me = models.TextField(max_length=500, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    avatar = models.ImageField(
        null=True,
        blank=True,
        upload_to=user_avatar_path,
    )
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(blank=True, null=True)
    USERNAME_FIELD = 'username'

    objects = UserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
