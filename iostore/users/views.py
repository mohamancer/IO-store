from django.shortcuts import render , redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import User
from .forms import MyUserCreationForm

# Create your views here.


def login_page(request):
    page = 'users-login'
    if request.user.is_authenticated:
        return redirect('feed-home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        # try:
        #     user = User.objects.get(username=username)
        # except:
        #     print("here")
        #     messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('feed-home')
        else:
            messages.error(request, 'Username OR password does not exit')

    context = {'page': page}
    return render(request, 'users/login_register.html' , context)

def logout_user(request):
    logout(request)
    return redirect('feed-home')


def register_page(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('feed-home')
        else:
            messages.error(request, 'An error occurred during registration')

    return render(request, 'users/login_register.html', {'form': form})