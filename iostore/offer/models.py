from django.db import models
from users.models import User


class Category(models.Model):

    class Meta:
        verbose_name_plural = "Categories"

    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Offer(models.Model):
    title = models.CharField(max_length=25)
    description = models.TextField(max_length=200)
    post_image = models.ImageField(null=True, upload_to="images/offer/",blank=True)
    final_bid = models.ForeignKey('Bid', on_delete=models.CASCADE,
                                  null=True, blank=True, related_name='final_bid')
    lowest_bid = models.FloatField(default=-1)
    host = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    reviewed_by_host = models.BooleanField(default=False)
    reviewed_by_bidder = models.BooleanField(default=False)
    bidding_deadline = models.DateTimeField(null=True)
    active = models.BooleanField(default=True)
    favorites = models.ManyToManyField(User, related_name='favorite', default=None, blank=True)
    address = models.CharField(verbose_name="Address",max_length=250, null=True, blank=True)
    longitude = models.CharField(verbose_name="Longitude",max_length=50, null=True, blank=True)
    latitude = models.CharField(verbose_name="Latitude",max_length=50, null=True, blank=True)
    distance_value = models.FloatField(verbose_name="Distance_value",max_length=50, null=True, blank=True)
    distance_text = models.CharField(verbose_name="Distance_text",max_length=50, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    price = models.FloatField()
    time_of_delivery = models.DateTimeField()
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, null=True)
    delivered= models.BooleanField(default=False)
    received = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.bidder.username + "'s bid"
