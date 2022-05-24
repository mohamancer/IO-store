from django.utils import timezone
from django.shortcuts import render, redirect
from django.db.models import Q
from offer.models import Offer, Bid, Category
import recommendation_system.calc_score

def home(request):
    bids = Bid.objects.all().order_by('-created')[0:2]
    offers = Offer.objects.all()
    all_offers_count = 0

    offers_to_be_delivered_and_received = Offer.objects.filter(final_bid__isnull=False)\
                                            .filter(final_bid__time_of_delivery__gt=timezone.now())\
                                            .order_by('final_bid__time_of_delivery')
    offers_to_be_reviewed_by_host = Offer.objects.filter(final_bid__isnull=False)\
                                        .filter(final_bid__time_of_delivery__lt=timezone.now()\
                                        ,reviewed_by_host=False).order_by('final_bid__time_of_delivery')
    offers_to_be_reviewed_by_bidder = Offer.objects.filter(final_bid__isnull=False)\
                                        .filter(final_bid__time_of_delivery__lt=timezone.now()\
                                        ,reviewed_by_bidder=False).order_by('final_bid__time_of_delivery')                                     

    q = request.GET.get('q') if request.GET.get('q') != None else ''
    categories = Category.objects.all()
    category_names = [c.name for c in categories]
    category_to_count = {}
    q1 = Offer.objects.all()
    for c in categories:
        cnt = q1.filter(category__id=c.id, active=True).count()
        if cnt != 0:
            category_to_count[c] = cnt
            all_offers_count += cnt
    flag = 0

    if q.lower() == "recommended":
        if not request.user.is_authenticated:
            return redirect('users-login')
        flag = 1
        user_id = request.user.id
        offers = recommendation_system.calc_score.get_recommanded_offers(user_id)
    elif q=='map':
        flag=3 
        offers = Offer.objects.filter(active=True)
    elif q in category_names:
        offers = Offer.objects.filter(
            Q(active=True) &
            Q(category__name__exact=q)
        ).order_by('-created')
    else:
        offers = Offer.objects.filter(
            Q(active=True) &
            (Q(category__name__icontains=q) |
             Q(title__icontains=q) |
             Q(description__icontains=q)|
             Q(host__username__icontains=q))
        ).order_by('-created')
    

    if type(offers) == type([0]):
        offer_count = len(offers)
    else:
        offer_count = offers.count()

    bids_per_offer = {}
    for offer in offers:
        local_bids = offer.bid_set.all()
        bids_per_offer[offer.id] = len(local_bids)


    context = {'offers': offers, 'categories': categories,
               'offer_count': offer_count, 'bids_per_offer': bids_per_offer,
               'all_offers_count': all_offers_count, 'bids': bids,
               'offers_to_be_delivered_and_received': offers_to_be_delivered_and_received,
                'category_to_count': category_to_count, 'offers_to_be_reviewed_by_host':offers_to_be_reviewed_by_host,
                'offers_to_be_reviewed_by_bidder':offers_to_be_reviewed_by_bidder, 'flag':flag}
    return render(request, 'feed/home.html', context)

def review(request, pk):
    if request.method == 'POST':
        offer = Offer.objects.get(id=pk)
        current_rating = request.POST.get('rating')
        if offer.host == request.user:
            bidder = offer.final_bid.bidder
            bidder.delivery_rating = (bidder.delivery_rating*bidder.delivery_number_of_reviews\
                                     + float(current_rating))/(bidder.delivery_number_of_reviews +1)
            bidder.delivery_number_of_reviews += 1
            offer.reviewed_by_host = True
            bidder.save()
        else:
            host = offer.host
            host.receiving_rating = (host.receiving_rating*host.receiving_number_of_reviews\
                                     + float(current_rating))/(host.receiving_number_of_reviews +1)
            host.receiving_number_of_reviews += 1
            offer.reviewed_by_bidder = True
            host.save() 
            
        offer.save()


    return redirect('feed-home')
