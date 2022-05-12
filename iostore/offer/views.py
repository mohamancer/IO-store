from django.shortcuts import render

def home(request, pk):
    offer = Offer.objects.get(id=pk)
    context = {'offer':offer}
    return render(request, 'offer/offer.html', context)

