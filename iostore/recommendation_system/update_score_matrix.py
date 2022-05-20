import threading
from offer.models import Offer, Bid
from users.models import User
from django.utils import timezone
from time import sleep
import numpy as np
import pandas as pd

from .calc_score import get_highest_rated_offers

matrix_df = pd.DataFrame()
last_updated = 0
s = set() # this set contains tuples of (user , offer) meaning the user already bidded on offer

def init_matrix():
    global s
    global matrix_df
    offers_amount = Offer.objects.all().count()
    users_amount = User.objects.all().count()
    matrix = np.zeros((users_amount,offers_amount))
    bid_list = Bid.objects.all()
    for bid in bid_list:
        bidder_id = bid.bidder.id - 1
        offer_id = bid.offer.id - 1
        if (bidder_id,offer_id) not in s:
            matrix[bidder_id][offer_id] += 2.0
            s.add((bidder_id,offer_id))
    matrix_df = pd.DataFrame(matrix)
    return matrix_df

def add_offer_columns_to_matrix_df(new_offers):
    global matrix_df
    for new_offer in new_offers:
        matrix_df.loc[len(matrix_df)] = 0.0

def add_user_rows_to_matrix_df(new_users):
    global matrix_df
    for new_user in new_users:
        matrix_df[len(matrix_df.columns)] = 0.0

def add_bids(new_bids):
    for bid in new_bids:
        bidder_id = bid.bidder.id - 1
        offer_id = bid.offer.id - 1
        if (bidder_id,offer_id) not in s:
            matrix_df[bidder_id][offer_id] += 2.0
            s.add((bidder_id,offer_id))

def update_matrix():
    # while true
    # filters offers, users, and bids made after a certain date
    global matrix_df
    global last_updated
    while True:
        new_users = User.objects.filter(date_joined__gte=last_updated)
        new_offers = Offer.objects.filter(created__gte=last_updated)
        new_bids = Bid.objects.filter(created__gte=last_updated)
        add_offer_columns_to_matrix_df(new_users)
        add_user_rows_to_matrix_df(new_offers)
        add_bids(new_bids)

        last_updated = timezone.now()
        sleep(10)

# def naiv_update_matrix():
#     #working
#     global matrix_df
#     global last_updated
#     global s
#     while True:
#         print(matrix_df)
#         s = set()
#         matrix_df = init_matrix()
#         #print(get_highest_rated_offers(matrix_df[5],matrix_df))
#         sleep(10)

def score_matrix_handler_thread():
    global matrix_df
    global last_updated
    matrix_df = init_matrix()
    last_updated = timezone.now()
    update_thread = threading.Thread(target=update_matrix, name='update_thread', daemon=True)
    update_thread.start()