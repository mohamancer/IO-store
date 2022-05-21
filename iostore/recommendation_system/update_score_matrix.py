import threading
from offer.models import Offer, Bid
from users.models import User
from django.utils import timezone
from time import sleep
import numpy as np
import pandas as pd
from scipy import spatial


matrix_df = pd.DataFrame()
last_updated = 0
s = set() # this set contains tuples of (user , offer) meaning the user already bidded on offer

bid_bonus = 5
fav_bonus = 3
viewed_bonus = 0

co_sim_matrix = []
prediction_matrix = pd.DataFrame()

def init_matrix():
    global s
    global matrix_df
    offers_amount = Offer.objects.all().count()
    users_amount = User.objects.all().count()
    matrix = np.ones((users_amount,offers_amount))
    bid_list = Bid.objects.all()
    for bid in bid_list:
        bidder_id = bid.bidder.id - 1
        offer_id = bid.offer.id - 1
        if (bidder_id,offer_id) not in s:
            matrix[bidder_id][offer_id] += bid_bonus
            s.add((bidder_id,offer_id))

    # need to update matrix every time a user adds something to favourites!!
    users = User.objects.all()
    for user in users:
        fav_offers = Offer.objects.filter(favorites=user)
        user_id = user.id - 1
        for fav_offer in fav_offers:
            fav_offer_id = fav_offer.id - 1
            matrix[user_id][fav_offer_id] += fav_bonus

    matrix_df = pd.DataFrame(matrix)
    return matrix_df

def add_offer_columns_to_matrix_df(new_offers):
    global matrix_df
    for new_offer in new_offers:
        matrix_df.loc[len(matrix_df)] = 1.0

def add_user_rows_to_matrix_df(new_users):
    global matrix_df
    for new_user in new_users:
        matrix_df[len(matrix_df.columns)] = 1.0

def add_bids(new_bids):
    for bid in new_bids:
        bidder_id = bid.bidder.id - 1
        offer_id = bid.offer.id - 1
        if (bidder_id,offer_id) not in s:
            matrix_df[offer_id][bidder_id] += bid_bonus #first [] should hold COLUMN INDEX and second ROW INDEX
            s.add((bidder_id,offer_id))

def update_users_offers_bids_in_matrix():
    global last_updated
    new_users = User.objects.filter(date_joined__gte=last_updated)
    new_offers = Offer.objects.filter(created__gte=last_updated)
    new_bids = Bid.objects.filter(created__gte=last_updated)
    
    add_offer_columns_to_matrix_df(new_users)
    add_user_rows_to_matrix_df(new_offers)
    add_bids(new_bids)

    last_updated = timezone.now()

def add_or_remove_from_fav(user_id,offer_id,is_add):
    global matrix_df
    user_index = user_id - 1
    offer_index = offer_id - 1
    update_users_offers_bids_in_matrix()
    try:
        if is_add:
            matrix_df[offer_index][user_index] += fav_bonus
        else:
            matrix_df[offer_index][user_index] -= fav_bonus
    except:
        pass


def update_user_offer_matrix():
    # while true
    # filters offers, users, and bids made after a certain date
    while True:
        print(matrix_df)
        update_users_offers_bids_in_matrix()
        sleep(5)

# def naiv_update_user_offer_matrix():
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


def construct_cos_similar_matrix(): #this can probably be done more efficiently
    global matrix_df
    global co_sim_matrix
    co_sim_matrix = pd.DataFrame(np.ones((len(matrix_df), len(matrix_df))))
    for i in range(len(matrix_df)):
        for j in range(len(matrix_df)):
            co_sim_matrix[j][i] = 1 - spatial.distance.cosine(matrix_df.iloc[i].tolist(), matrix_df.iloc[j].tolist())

    #co_sim_matrix = sklearn.metrics.pairwise.cosine_similarity(matrix_df)
    return co_sim_matrix

def calc_weighted_score(j):
    global co_sim_matrix
    global matrix_df
    global prediction_matrix
    # j is the offer
    # i is the user
    numerator = 0.0
    denominator = 0.0
    for i in range(len(co_sim_matrix)): # go over all people
        if matrix_df[j][i] != 0:
            numerator += co_sim_matrix[j][i] * matrix_df[j][i]
            denominator += co_sim_matrix[j][i] # this might have to go inside the if!!!!
            # im putting it outside because currently our "like function" is really dumb, taking into considration only if a offer was bidded or not.
        numerator -= co_sim_matrix[j][i]/5 # might have to delete this when i have a better like function, watch this: https://www.youtube.com/watch?v=Fmtorg_dmM0&ab_channel=ritvikmath
        
    if denominator != 0:
        return (numerator / denominator)
    else: # if there are no users who rated this offer, deominator will be 0
        return 0

def construct_prediction_matrix():
    global matrix_df
    global co_sim_matrix
    global prediction_matrix
    # co_sim_matrix is of same size like matrix_df
    prediction_matrix = pd.DataFrame(np.ones((len(matrix_df), len(matrix_df.iloc[0]))))
    for i in range(len(prediction_matrix)):
        for j in range(len(prediction_matrix.iloc[0])):
            # if matrix_df[j][i] != 1:
            #     prediction_matrix[j][i] = matrix_df[j][i]
            # else:
            #     prediction_matrix[j][i] = calc_weighted_score(j)
            prediction_matrix[j][i] = calc_weighted_score(j)

def construct_all_matrices():
    if len(matrix_df) >= 1:
        construct_cos_similar_matrix()
        construct_prediction_matrix()

    #print(prediction_matrix)

def update_prediction_and_cos_matrices():
    while True:
        construct_all_matrices()
        sleep(20)


def matrices_handler_thread():
    global matrix_df
    global last_updated
    # while(True):
    #     offers_amount = Offer.objects.all().count()
    #     users_amount = User.objects.all().count()
    #     if offers_amount >= 2 and users_amount >= 2:
    #         break
    #     sleep(5)

    matrix_df = init_matrix()
    last_updated = timezone.now()
    user_offer_update_thread = threading.Thread(target=update_user_offer_matrix, name='user_offer_update_thread', daemon=True)
    user_offer_update_thread.start()

    prediction_and_cos_matrices_thread = threading.Thread(target=update_prediction_and_cos_matrices, name='update_prediction_and_cos_matrices',daemon=True)
    prediction_and_cos_matrices_thread.start()