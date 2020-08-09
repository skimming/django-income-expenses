from django.db import models

# Create your models here.
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)

from rest_framework_simplejwt.tokens import RefreshToken

# derived from auto.models
# exposes methods for creating users and superusers
class UserManager(BaseUserManager) :
    def create_user(self, username, email, password=None):
        if username is None: 
            raise TypeError('Users should have a username')
        if email is None: 
            raise TypeError('Users should have a email')
        if password is None: 
            raise TypeError('Users should have a password')

        user=self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password=None):
        if username is None: 
            raise TypeError('Users should have a username')
        if email is None: 
            raise TypeError('Users should have a email')
        if password is None: 
            raise TypeError('Users should have a password')
        
        user=self.create_user(username, email, password)
        user.is_superuser=True
        user.is_staff=Trueuser.save()
        return user


# this is the model for the class
class User(AbstractBaseUser,PermissionsMixin) :
    username = models.CharField(max_length=255, unique=True, db_index=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'  # when logging in, we will be using the email as the username
    REQUIRED_FIELDS = ['username']

    # identify the manager for User
    # manager will have a create_user
    objects = UserManager()

    # to satisfy the tostring?
    def __str__(self):
        return f"name [{self.username}], email [{self.email}]"

    # to retrieve all the tokens for the user
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

