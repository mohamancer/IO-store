from unicodedata import category
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .forms import OfferForm
from .models import Offer, Category, Bid
# Create your views here.


def offer(request, pk):
    offer = Offer.objects.get(id=pk)
    # room_messages = room.message_set.all()
    # participants = room.participants.all()

    # if request.method == 'POST':
    #     message = Message.objects.create(
    #         user=request.user,
    #         room=room,
    #         body=request.POST.get('body')
    #     )
    #     room.participants.add(request.user)
    #     return redirect('room', pk=room.id)

    context = {'offer': offer}
    return render(request, 'offer/offer.html', context)

@login_required(login_url='users-login')
def createOffer(request):
    form = OfferForm()
    categories = Category.objects.all()
    if request.method == 'POST':
        category_name = request.POST.get('category')
        category, created = Category.objects.get_or_create(name=category_name)

        Offer.objects.create(
            host=request.user,
            category=category,
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            bidding_deadline = request.POST.get('bidding_deadline')
        )
        return redirect('feed-home')

    context = {'form': form, 'categories': categories}
    return render(request, 'offer/offer_form.html', context)

@login_required(login_url='users-login')
def updateOffer(request, pk):
    offer = Offer.objects.get(id=pk)
    form = OfferForm(instance=offer)
    categories = category.objects.all()
    if request.user != offer.host:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        category_name = request.POST.get('category')
        category, created = Category.objects.get_or_create(name=category_name)
        offer.name = request.POST.get('title')
        offer.category = category
        offer.description = request.POST.get('description')
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
