from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
import uuid
from PIL import Image, ImageDraw, ImageFont
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO


class UserManager(BaseUserManager):
    def create_user(self, username, email=None, password=None):
        if not email:
            raise ValueError("Users Must Have an email address")
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
        user.save(using=self._db)
        return user


class Users(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=20, unique=True)
    profile_image = models.ImageField(null=True, blank=True, upload_to='profile_photos/')
    password = models.CharField(max_length=128)
    email = models.EmailField(unique=False, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    birthday = models.DateField(null=True, blank=True)
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    reset_code = models.CharField(max_length=10, blank=True, null=True)
    reset_code_expiry = models.DateTimeField(blank=True, null=True)

    objects = UserManager()
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    class Meta:
        app_label = 'users'
        db_table = 'users'
