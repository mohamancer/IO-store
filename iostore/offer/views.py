from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import OfferForm
from .models import Offer, Category, Bid


def offer(request, pk):
    offer = Offer.objects.get(id=pk)
    offer_bids = offer.bid_set.all().order_by('-created')

    if request.method == 'POST':
        bid = Bid.objects.create(
            bidder=request.user,
            offer=offer,
            price=request.POST.get('price'),
            time_of_delivery=request.POST.get('time_of_delivery')
        )
        if offer.lowest_bid == -1:
            offer.lowest_bid = float(request.POST.get('price'))
        else:
            offer.lowest_bid = min(
                offer.lowest_bid, float(request.POST.get('price')))
        offer.save()
        return redirect('offer', pk=offer.id)

    context = {'offer': offer, 'offer_bids': offer_bids}
    return render(request, 'offer/offer.html', context)


@login_required(login_url='users-login')
def createOffer(request):
    form = OfferForm()
    categories = Category.objects.all()
    if request.method == 'POST':
        category_name = request.POST.get('category')
        category = Category.objects.get(id=category_name)
        Offer.objects.create(
            host=request.user,
            category=category,
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            bidding_deadline=request.POST.get('bidding_deadline')
        )
        return redirect('feed-home')

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
        category_name = request.POST.get('category')
        category = Category.objects.get(id=category_name)
        offer.title = request.POST.get('title')
        offer.category = category
        offer.description = request.POST.get('description')
        offer.bidding_deadline = request.POST.get('bidding_deadline')
        offer.save()
        return redirect('feed-home')

    context = {'form': form, 'categories': categories, 'offer': offer}
    return render(request, 'offer/offer_form.html', context)


@login_required(login_url='users-login')
def deleteOffer(request, pk):
    offer = Offer.objects.get(id=pk)

    if request.user != offer.host:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
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
