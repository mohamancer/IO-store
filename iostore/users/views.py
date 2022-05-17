from django.shortcuts import render , redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import User
from offer.models import Category, Offer
from .forms import my_user_creation_form, update_user_form, user_login_form
from django.contrib.auth.decorators import login_required
from django.db.models import Q

# Create your views here.


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
    return render(request, 'users/login_register.html' , context)

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
    all_offers_count = Offer.objects.all().count()
    temp = Offer.objects.all().order_by('-created')
    offers = []
    for offer in temp:
        if offer.host.username == pk:
            offers.append(offer)

    bids_per_offer = {}
    for offer in offers:
        bids = offer.bid_set.all()
        bids_per_offer[offer.id]= len(bids)

    user = User.objects.get(username=pk)
    context = {'user': user, 'categories': categories, 'all_offers_count': all_offers_count, 'offers': offers, 'bids_per_offer': bids_per_offer}
    return render(request, 'users/profile.html', context)


    