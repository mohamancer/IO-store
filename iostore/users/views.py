from django.conf import Settings, settings
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Address, User
from offer.models import Category, Offer
from .forms import my_user_creation_form, update_address_form, update_user_form, user_login_form
from django.contrib.auth.decorators import login_required


def login_page(request):
    page = 'users-login'
    login_form = user_login_form()

    if request.user.is_authenticated:
        return redirect('feed-home')

    if request.method == 'POST':
        login_form = user_login_form(request.POST)
        if login_form.is_valid():
            username = request.POST.get('username').lower()
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('feed-home')
            else:
                messages.error(request, 'Username OR password does not exit')
        else:
            messages.error(request, 'An error occurred during login')

    context = {'page': page, 'login_form': login_form}
    return render(request, 'users/login_register.html', context)


def logout_user(request):
    logout(request)
    return redirect('feed-home')


def register_page(request):
    form = my_user_creation_form()

    if request.method == 'POST':
        form = my_user_creation_form(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('feed-home')
        else:
            messages.error(request, 'An error occurred during registration')

    return render(request, 'users/login_register.html', {'form': form})


@login_required(login_url='users-login')
def update_profile(request):
    user = request.user
    form = update_user_form(instance=user)

    if request.method == 'POST':
        form = update_user_form(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('users-profile', pk=user.username)

    return render(request, 'users/update_profile.html', {'form': form})


def profile_page(request, pk):
    categories = Category.objects.all()
    all_offers_count = 0
    temp = Offer.objects.all().order_by('-created')
    offers_to_be_delivered_and_received = Offer.objects.filter(final_bid__isnull=False)\
        .order_by('final_bid__time_of_delivery')
    offers = []
    for offer in temp:
        if offer.host.username == pk:
            offers.append(offer)

    bids_per_offer = {}
    for offer in offers:
        bids = offer.bid_set.all()
        bids_per_offer[offer.id] = len(bids)

    category_to_count = {}
    q1 = Offer.objects.all()
    for c in categories:
        cnt = q1.filter(category__id=c.id, active=True).count()
        if cnt != 0:
            category_to_count[c] = cnt
            all_offers_count += cnt

    user = User.objects.get(username=pk)
    context = {'user': user, 'category_to_count': category_to_count,
               'all_offers_count': all_offers_count, 'offers': offers,
               'bids_per_offer': bids_per_offer, 'offers_to_be_delivered_and_received': offers_to_be_delivered_and_received}
    return render(request, 'users/profile.html', context)

@ login_required
def favorite_add(request, id):
    post = get_object_or_404(Offer, id=id)
    if post.favorites.filter(id=request.user.id).exists():
        post.favorites.remove(request.user)
    else:
        post.favorites.add(request.user)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

@ login_required
def favorite_list(request):
    offers_to_be_delivered_and_received = Offer.objects.filter(final_bid__isnull=False)\
        .order_by('final_bid__time_of_delivery')
    offers = Offer.objects.filter(favorites=request.user).order_by('-created')
    categories = Category.objects.all()
    all_offers_count = 0
    category_to_count = {}
    q1 = Offer.objects.all()
    for c in categories:
        cnt = q1.filter(category__id=c.id, active=True).count()
        if cnt != 0:
            category_to_count[c] = cnt
            all_offers_count += cnt
    bids_per_offer = {}
    offer_count = 0
    for offer in offers:
        offer_count += 1
        local_bids = offer.bid_set.all()
        bids_per_offer[offer.id] = len(local_bids)
    return render(request, 'users/favorites.html', {'offer_count':offer_count,'offers_to_be_delivered_and_received':offers_to_be_delivered_and_received,'offers': offers, 'bids_per_offer': bids_per_offer, 'category_to_count':category_to_count,'all_offers_count': all_offers_count})

@login_required
def update_address(request):
    form = update_address_form()
    if request.method == 'POST':
        form = update_address_form(request.POST)
        Address.objects.create(
            address = form.fields.get('address'),
            longitude = form.fields.get('longitude'),
            latitude = form.fields.get('latitude'),
            user = request.user
        )
        return redirect('users-profile', pk=request.user.username)

    return render(request, 'users/update_address.html', {'form': form, 'google_api_key': settings.GOOGLE_API_KEY})