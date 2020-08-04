from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


# ****** Custom UserManager Model ******
class UserManager(BaseUserManager):

    # Creating user
    def create_user(self, username, email, password=None, is_active=True, is_staff=False, is_admin=False):
        if not username:
            return ValueError('User must have a username.')
        if not email:
            return ValueError('User must have a email address.')
        if not password:
            return ValueError('User must have a password.')

        email = self.normalize_email(email)
        user_obj = self.model(username=username, email=email)
        user_obj.set_password(password)

        user_obj.is_active = is_active
        user_obj.is_staff = is_staff
        user_obj.is_admin = is_admin

        user_obj.save(using=self._db)
        return user_obj

    # Creating staff
    def create_staff(self, username, email, password=None):
        user = self.create_user(
            username=username, email=email, password=password, is_staff=True)
        return user

    # Creating superuser
    def create_superuser(self, username, email, password=None):
        user = self.create_user(
            username=username, email=email, password=password, is_staff=True, is_admin=True)
        return user


# ****** Custom User Model ******
class User(AbstractBaseUser):

    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'username',
    ]

    objects = UserManager()

    def __str__(self):
        return self.username

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
