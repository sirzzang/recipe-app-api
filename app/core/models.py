from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin


class UserManager(BaseUserManager): # extends BaseUserManager

    def create_user(self, email, password=None, **extra_fields):
        '''Create and saves a new user'''
        if not email: # email validation
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), \
            **extra_fields) # add normalizing helper function
        user.set_password(password) # helper function in AbstractBaseUser
        user.save(using=self._db) # supporting multiple databases

        return user

    def create_superuser(self, email, password): # superuser feature added
        '''create and saves a super user'''
        user = self.create_user(email, password) # create user
        # staff, superuser
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db) # save user

        return user
        

class User(AbstractBaseUser, PermissionsMixin):
    '''Custom user model that supports using email instead of username'''
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email' # default user name field is email
