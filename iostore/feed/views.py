from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from offer.models import Offer, Bid, Category

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    offers = Offer.objects.filter(
        Q(active=True) &
        (Q(category__name__icontains=q) |
        Q(title__icontains=q) |
        Q(description__icontains=q))
    ).order_by('-created')
    categories = Category.objects.all()
    offer_count = offers.count()

    bids_per_offer = {}
    for offer in offers:
        bids = offer.bid_set.all()
        bids_per_offer[offer.id]= len(bids)
    
    context = {'offers': offers, 'categories': categories,
               'offer_count': offer_count,'bids_per_offer':bids_per_offer}
    return render(request, 'feed/home.html', context)


