from django.conf import settings
from django.utils import timezone
from django.shortcuts import render, redirect
from django.db.models import Q
from offer.models import Offer, Bid, Category
from users.models import Rating
import recommendation_system.calc_score
import googlemaps


def home(request):
    google_api_key = settings.GOOGLE_API_KEY
    near_me_flag = False
    distance_filter = 50000
    if not request.user.is_authenticated:
        Offer.objects.all().update(distance_value = None, distance_text = '')
    else:
        offers = Offer.objects.filter(
            Q(active=True))
        user_location = (float(request.user.latitude), float(request.user.longitude))
        gmaps = googlemaps.Client(key=google_api_key)
        if (request.user.changed_address):
            offers = Offer.objects.filter(active=True)
        else:
            offers = Offer.objects.filter(active=True, distance_value=None)
        for offer in offers:
            offer_location = (offer.latitude, offer.longitude)
            distance_result = gmaps.distance_matrix(user_location, offer_location)
            offer.distance_text = distance_result["rows"][0]["elements"][0]["distance"]["text"]
            offer.distance_value = distance_result["rows"][0]["elements"][0]["distance"]["value"]
            request.user.changed_address=False
            request.user.save()
            offer.save()



    bids = Bid.objects.all().order_by('-created')[0:2]
    offers = Offer.objects.all()
    all_offers_count = 0

    offers_to_be_delivered_and_received = Offer.objects.filter(Q(final_bid__isnull=False)&
                                            Q(final_bid__time_of_delivery__gt=timezone.now()))\
                                            .order_by('final_bid__time_of_delivery')
    offers_to_be_reviewed_by_host = Offer.objects.filter((Q(final_bid__isnull=False) &
                                        Q(final_bid__time_of_delivery__lt=timezone.now()) &
                                        Q(reviewed_by_host=False)) |( Q(reviewed_by_host=False) & Q(final_bid__received=True))).order_by('final_bid__time_of_delivery')
    offers_to_be_reviewed_by_bidder = Offer.objects.filter((Q(final_bid__isnull=False) &
                                        Q(final_bid__time_of_delivery__lt=timezone.now()) &
                                        Q(reviewed_by_bidder=False)) |( Q(reviewed_by_bidder=False) & Q(final_bid__delivered=True))).order_by('final_bid__time_of_delivery')  


    for offer in offers_to_be_reviewed_by_host:
        offer.final_bid.received = True
        offer.final_bid.save()
        offer.save()
    for offer in offers_to_be_reviewed_by_bidder:
        offer.final_bid.delivered = True
        offer.final_bid.save()
        offer.save()


    q = request.GET.get('q') if request.GET.get('q') != None else ''
    distance_filter = int(request.GET.get('d'))*1000 if request.GET.get('d') != None else 50000
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
        if not request.user.is_authenticated:
            return redirect('users-login')
        flag=3 
        offers = Offer.objects.filter(active=True)
    elif q in category_names:
        offers = Offer.objects.filter(
            Q(active=True) &
            Q(category__name__exact=q)
        ).order_by('-created')
    elif q=='near_me':
        if not request.user.is_authenticated:
            return redirect('users-login')
        offers = Offer.objects.filter(
            Q(active=True) &
            (Q(distance_value__lte = distance_filter))
        ).order_by('distance_value')
        near_me_flag = True
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
               'offers_to_be_reviewed_by_bidder':offers_to_be_reviewed_by_bidder, 'flag':flag,
               'near_me_flag': near_me_flag, 'distance_filter': distance_filter/1000}
    return render(request, 'feed/home.html', context)

def review(request, pk):
    if request.method == 'POST':
        offer = Offer.objects.get(id=pk)
        current_rating = request.POST.get('rating')

        if offer.host == request.user:
            bidder = offer.final_bid.bidder
            if bidder.delivery_number_of_reviews==0:
                bidder.delivery_rating = Rating.objects.create()

            bidder.delivery_rating = calc_rating(request, pk)
            print(bidder.delivery_rating)
            bidder.delivery_number_of_reviews += 1
            offer.reviewed_by_host = True

            bidder.delivery_rating.save()
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

def calc_rating(request, pk):
    offer = Offer.objects.get(id=pk)
    bidder = offer.final_bid.bidder

    current_acc_rating = request.POST.get('rating1')
    current_qulaity_rating = request.POST.get('rating2')
    current_arrival_rating = request.POST.get('rating3')
    current_cost_rating = request.POST.get('rating4')

    bidder.delivery_rating.accuracy_rating = (bidder.delivery_rating.accuracy_rating*bidder.delivery_number_of_reviews\
                            + float(current_acc_rating))/(bidder.delivery_number_of_reviews +1)
    bidder.delivery_rating.quality_rating = (bidder.delivery_rating.quality_rating*bidder.delivery_number_of_reviews\
                        + float(current_qulaity_rating))/(bidder.delivery_number_of_reviews +1)
    bidder.delivery_rating.arrival_rating = (bidder.delivery_rating.arrival_rating*bidder.delivery_number_of_reviews\
                        + float(current_arrival_rating))/(bidder.delivery_number_of_reviews +1)   
    bidder.delivery_rating.cost_rating = (bidder.delivery_rating.cost_rating*bidder.delivery_number_of_reviews\
                        + float(current_cost_rating))/(bidder.delivery_number_of_reviews +1)
    bidder.delivery_rating.avg = (bidder.delivery_rating.accuracy_rating + bidder.delivery_rating.quality_rating\
        + bidder.delivery_rating.arrival_rating + bidder.delivery_rating.cost_rating)/4 


    return bidder.delivery_rating            