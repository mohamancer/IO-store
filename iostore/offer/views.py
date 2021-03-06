import datetime
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import pytz
from .forms import OfferForm, update_address_form_offer
from .models import Offer, Category, Bid
from recommendation_system.update_score_matrix import user_clicked_on_offer
import pickle
from django.utils import timezone
amount_of_deleted_offers_file = 'amount_of_deleted_offers_file.pkl'

@login_required(login_url='users-login')
def offer(request, pk):
    offer = Offer.objects.get(id=pk)
    offer_bids = offer.bid_set.all().order_by('-created')
    fav_off = Offer.objects.filter(favorites=request.user)
    if offer in fav_off:
        is_in_fav = True
    else:
        is_in_fav = False
    
    user_clicked_on_offer(request.user.id,offer.id)

    if request.method == 'POST':
        time_of_delivery_tz = gettimezone(request.POST.get('time_of_delivery'))
        bid = Bid.objects.create(
            bidder=request.user,
            offer=offer,
            price=request.POST.get('price'),
            time_of_delivery=time_of_delivery_tz
        )
        if offer.lowest_bid == -1:
            offer.lowest_bid = float(request.POST.get('price'))
        else:
            offer.lowest_bid = min(
                offer.lowest_bid, float(request.POST.get('price')))
        offer.save()
        return redirect('offer', pk=offer.id)

    context = {'offer': offer, 'offer_bids': offer_bids, 'is_in_fav': is_in_fav}
    return render(request, 'offer/offer.html', context)


@login_required(login_url='users-login')
def createOffer(request):
    form = OfferForm()
    categories = Category.objects.all()
    if request.method == 'POST':
        bidding_deadline_tz = gettimezone(request.POST.get('bidding_deadline'))
        category_name = request.POST.get('category')
        category = Category.objects.get(id=category_name)
        offer = Offer.objects.create(
            host=request.user,
            category=category,
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            bidding_deadline = bidding_deadline_tz,
            post_image = request.FILES.get('post_image')
        )

        return redirect('create-address-offer', pk=offer.id)

    context = {'form': form, 'categories': categories}
    return render(request, 'offer/offer_form.html', context)


@login_required(login_url='users-login')
def updateOffer(request, pk):
    offer = Offer.objects.get(id=pk)
    form = OfferForm(instance=offer)
    categories = Category.objects.all()
    if request.user != offer.host:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        bidding_deadline_tz = gettimezone(request.POST.get('bidding_deadline'))
        category_name = request.POST.get('category')
        category = Category.objects.get(id=category_name)
        offer.title = request.POST.get('title')
        offer.category = category
        offer.description = request.POST.get('description')
        offer.bidding_deadline = bidding_deadline_tz 
        if request.FILES.get('post_image'):
            offer.post_image = request.FILES.get('post_image')
        offer.save()
        return redirect('offer', pk=offer.id)

    context = {'form': form, 'categories': categories, 'offer': offer}
    return render(request, 'offer/offer_form.html', context)


@login_required(login_url='users-login')
def deleteOffer(request, pk):
    offer = Offer.objects.get(id=pk)

    if request.user != offer.host:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        amount_of_deleted_offers = [0]
        with open(amount_of_deleted_offers_file, 'rb') as f:
            amount_of_deleted_offers = pickle.load(f)
        pickle.dump([amount_of_deleted_offers[0]+1],open(amount_of_deleted_offers_file,'wb'))
        offer.delete()
        return redirect('feed-home')
    return render(request, 'offer/delete.html', {'obj': offer})


@login_required(login_url='users-login')
def deleteBid(request, pk):
    bid = Bid.objects.get(id=pk)

    if request.user != bid.bidder:
        return HttpResponse('Your are not allowed here!!')
    if request.method == 'POST':
        bid.delete()
        remaining_bids = Bid.objects.all().filter(offer=bid.offer)
        mn = float('inf')
        for remaning_bid in remaining_bids:
            mn = min(mn, remaning_bid.price)
        bid.offer.lowest_bid = mn
        if mn == float('inf'):
            bid.offer.lowest_bid = -1
        bid.offer.save()
        return redirect('offer', pk=bid.offer.id)
    return render(request, 'offer/delete.html', {'obj': bid})


@login_required(login_url='users-login')
def acceptBid(request, pk):
    bid = Bid.objects.get(id=pk)
    if request.user != bid.offer.host:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        bid.offer.final_bid = bid
        bid.offer.active = False
        bid.offer.save()
    return redirect('offer', pk=bid.offer.id)

@login_required(login_url='users-login')
def create_address_offer(request, pk):
    user = request.user
    offer=Offer.objects.get(id=pk)
    offer.address = user.address
    offer.longitude = user.longitude
    offer.latitude = user.latitude
    offer.save()
    form = update_address_form_offer(instance=offer)
    if request.method == 'POST':
        offer=Offer.objects.get(id=pk)
        form = update_address_form_offer(request.POST, instance=offer)
        if form.is_valid():
            form.save()
            offer.save()
            return redirect('offer',pk=offer.id)
    return render(request, 'offer/update_offer_address.html', {'offer':offer,'form': form,
                                                             'google_api_key': settings.GOOGLE_API_KEY})


def changeBidTime(request, pk):
    bid = Bid.objects.get(id=pk)
    if request.method == 'POST':
        next = request.POST.get('next', '/')
        if request.user == bid.bidder:
            bid.delivered = True
        else:
            bid.received = True
        bid.save()
    return redirect(next)

def gettimezone(date_as_string):
    parsed_date = datetime.datetime.strptime(date_as_string, '%Y-%m-%dT%H:%M')
    israel_timezone = pytz.timezone('Israel')
    date_time = israel_timezone.localize(parsed_date)
    return date_time
