from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models
import uuid


class UserManager(BaseUserManager):
    def create_user(self, username, email=None, password=None):
        if not username:
            raise ValueError("Users Must Have a username")
        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        if password is None:
            raise TypeError("Superusers must have a password.")
        user = self.create_user(username=username, email=email, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class Users(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=20, unique=True)
    online = models.BooleanField(default=False)
    password = models.CharField(max_length=100)
    email = models.EmailField(unique=False, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    birthday = models.DateField(null=True, blank=True)
    my_followers = models.IntegerField(default=0)
    follow = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    reset_code = models.CharField(max_length=10, blank=True, null=True)
    reset_code_expiry = models.DateTimeField(blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

    def formatted_birthday(self):
        if self.birthday:
            return self.birthday.strftime('%Y-%m-%d')
        return ''

    class Meta:
        app_label = 'users'
        db_table = 'users'
