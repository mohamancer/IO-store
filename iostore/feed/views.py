from django.shortcuts import render

posts = [
    {'id':1, 'item':'Signet Hammer'},
    {'id':2, 'item':'Bamaba Hammer'},
    {'id':3, 'item':'SpaceX Rocket'},
]

def home(request):
    context = {'posts':posts}
    return render(request, 'feed/home.html', context)

def post(request, pk):
    post = None
    for i in posts:
        if i['id'] == int(pk):
            post = i
    context = {'post':post}
    return render(request, 'feed/post.html', context)
