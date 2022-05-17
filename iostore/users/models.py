from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(
        unique=True, max_length=15, null=True, blank=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(default='avatar.svg', null=True)
    rating = models.FloatField(blank=True,null=True)
    number_of_reviews = models.IntegerField(default=0,blank=True)
    is_dark_mode = models.BooleanField(default = True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
