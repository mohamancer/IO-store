import py_compile
import threading
from .models import Offer, Bid
from django.utils import timezone
from time import sleep

def mark_offers_inactive_by_deadline():   
    try:
        make_inactive = Offer.objects.filter(bidding_deadline__lte=timezone.now() , active = True)
        for to_make_inactive_offer in make_inactive:
            to_make_inactive_offer.active = False
            to_make_inactive_offer.save()
    except:
        pass

def periodically_mark_offers_inactive_by_deadline():
    while True:
        mark_offers_inactive_by_deadline()
        sleep(60)

def periodically_mark_offers_inactive_by_deadline_thread():
    update_thread = threading.Thread(target=periodically_mark_offers_inactive_by_deadline, name='update_thread', daemon=True)
    update_thread.start()