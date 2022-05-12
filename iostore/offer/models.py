from django.db import models
from users.models import User

class Offer(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    item = models.CharField(max_length=200)
    category = models.PositiveSmallIntegerField()
    description = models.TextField(max_length=600)
    seen = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    final_bid = models.ForeignKey(Bid , on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return self.item

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=100, decimal_places=2)
    eta = models.DateTimeField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.price)
