from django.db import models
from users.models import User
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self):
        return self.name
    

class Post(models.Model):
    title = models.CharField(max_length = 25)
    description = models.TextField()
    post_image = models.ImageField(default='a.png',blank=True)
    final_bid = models.ForeignKey('Bid' , on_delete=models.CASCADE,
        null=True,blank=True, related_name='final_bid')
    host = models.ForeignKey(User, on_delete=models.CASCADE,null=True, related_name='host')
    provider = models.ForeignKey(User, on_delete=models.CASCADE,null=True, related_name='provider')
    category = models.ForeignKey(Category,on_delete=models.CASCADE,null=True)
    date_of_creation = models.DateTimeField(auto_now_add=True)    
    bidding_deadline = models.DateTimeField(null=True)
    active = models.BooleanField(default = True)
    
    def __str__(self):
        return self.title

class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    offer = models.FloatField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE,null=True)
    date_of_bid = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    def __str__(self):
        return self.bidder.username + ' has bid ' + str(self.offer) 