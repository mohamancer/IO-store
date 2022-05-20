from django.shortcuts import render, redirect
from django.db.models import Q
from offer.models import Offer, Bid, Category
import recommendation_system.calc_score

def home(request):
    bids = Bid.objects.all().order_by('-created')[0:2]
    offers = Offer.objects.all()
    all_offers_count = 0

    offers_to_be_delivered_and_received = Offer.objects.filter(final_bid__isnull=False)\
        .order_by('final_bid__time_of_delivery')

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

    if q.lower() == "recommended":
        import recommendation_system.update_score_matrix
        user_id = request.user.id - 1
        best_match_ids = recommendation_system.calc_score.get_highest_rated_offers(recommendation_system.update_score_matrix.matrix_df.iloc[user_id],recommendation_system.update_score_matrix.matrix_df)
        offers = []
        for offer_id in best_match_ids:
            offers.append(Offer.objects.get(id = offer_id))
        #print(offers)

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
             Q(description__icontains=q))
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
               'offers_to_be_delivered_and_received': offers_to_be_delivered_and_received, 'category_to_count': category_to_count}
    return render(request, 'feed/home.html', context)
