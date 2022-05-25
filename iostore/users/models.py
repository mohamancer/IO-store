from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(
        unique=True, max_length=15, null=True, blank=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(
        default='avatar.svg', null=True, upload_to='images/users/')
    delivery_rating = models.FloatField(default=0, blank=True)
    delivery_number_of_reviews = models.IntegerField(default=0, blank=True)
    receiving_rating = models.FloatField(default=0, blank=True)
    receiving_number_of_reviews = models.IntegerField(default=0, blank=True)
    is_dark_mode = models.BooleanField(default=True)
    address = models.CharField(verbose_name="Address",max_length=250, null=True, blank=True)
    longitude = models.CharField(verbose_name="Longitude",max_length=50, null=True, blank=True)
    latitude = models.CharField(verbose_name="Latitude",max_length=50, null=True, blank=True)
    changed_address = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
