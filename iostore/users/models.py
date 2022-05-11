from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15,null=True,blank=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(default='users/images/avatar.svg', null=True, blank=True)
    rating = models.FloatField(blank=True,null=True)
    number_of_reviews = models.IntegerField(default=0,blank=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []