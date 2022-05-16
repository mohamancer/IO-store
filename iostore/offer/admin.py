from django.contrib import admin
from .models import Offer, Bid, Category
# Register your models here.

admin.site.register(Offer)
admin.site.register(Bid)
admin.site.register(Category)