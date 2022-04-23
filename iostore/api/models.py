from email.policy import default
from django.db import models
import datetime
from django.contrib.auth.models import AbstractUser

# Create your models here.
"""
class User(AbstractUser):
    first_name= models.CharField(null=True, max_length=100)
    last_name = models.CharField(null=True, max_length=100)
    email = models.EmailField(unique=True ,null =True)
    bio = models.TextField(null=True,blank=True)
    avatar = models.ImageField(null=True,blank=True)
    number_of_reviews = models.IntegerField(default=0,blank=True)
    rating = models.FloatField(blank=True,null=True)
    #phone_number = models.CharField(max_length=15)
    #highlighted_requests
"""
class User(AbstractUser):
    
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(blank=True)

    avatar = models.ImageField(default='a.png',blank=True)
    rating = models.FloatField(blank=True,null=True)
    number_of_reviews = models.IntegerField(default=0,blank=True)
    phone_number = models.CharField(max_length=15,null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']   


class Category(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self):
        return self.name
    

class Request(models.Model):
    title = models.CharField(max_length = 25)
    # slug = models.SlugField()
    description = models.TextField()
    final_bid = models.ForeignKey('Bid' , on_delete=models.CASCADE,null=True,blank=True)
    Host = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,null=True)
    date_of_creation = models.DateTimeField(auto_now_add=True)    
    bidding_deadline = models.DateTimeField(null=True)
    is_relevant = models.BooleanField(default = True)
    
    def __str__(self):
        return self.title

class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    offer = models.FloatField()
    transaction = models.ForeignKey(Request, on_delete=models.CASCADE,null=True)
    date_of_bid = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    def __str__(self):
        return self.bidder.username

