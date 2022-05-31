import threading
from offer.models import Offer, Bid
from users.models import User
from django.utils import timezone
from time import sleep
import numpy as np
import pandas as pd
from scipy import spatial
import pickle

matrix_df = pd.DataFrame() # this dataframe will hold user's love for an offer not including amount of clicks per offer
last_updated = 0
s = set() # this set contains tuples of (user , offer) meaning the user already bidded on offer

bid_bonus = 5
fav_bonus = 3
clicks_bonus = 2

co_sim_matrix = []
prediction_matrix = pd.DataFrame()


users_clicks = dict() # this is a dictionary mapping user to min(3,number of clicks on the post)
amount_of_deleted_offers = [5]

users_clicks_file = 'users_clicks_file.pkl'
amount_of_deleted_offers_file = 'amount_of_deleted_offers_file.pkl'


def read_click_dict():
    global users_clicks
    try:
        with open(users_clicks_file, 'rb') as f:
            users_clicks = pickle.load(f)
    except:
        users_clicks = dict()

def save_click_dict():
    global users_clicks
    if len(users_clicks)>=1:
        with open(users_clicks_file, 'wb') as f:
            pickle.dump(users_clicks, f)


def user_clicked_on_offer(user_id,offer_id):
    if (user_id,offer_id) in users_clicks:
        users_clicks[(user_id,offer_id)] = min(users_clicks[(user_id,offer_id)]+1,clicks_bonus)
    else:
        users_clicks[(user_id,offer_id)] = 1

def get_real_user_love_for_offer(user_id,offer_id):
    love = matrix_df[offer_id][user_id]
    if (user_id,offer_id) in users_clicks:
        love += users_clicks[(user_id,offer_id)]
    return love

def print_real_love(): #just for testing, not really using this
    love_matrix = np.ones((len(matrix_df),len(matrix_df.iloc[0])))
    for i in range(len(matrix_df)):
        for j in range(len(matrix_df.iloc[0])):
            love_matrix[i][j] = get_real_user_love_for_offer(i,j)


def init_matrix():
    global s
    global matrix_df
    amount_of_deleted_offers = [0]
    try:
        with open(amount_of_deleted_offers_file, 'rb') as f:
            amount_of_deleted_offers = pickle.load(f)
    except:
        pickle.dump(amount_of_deleted_offers,open(amount_of_deleted_offers_file,'wb'))
        


    offers_amount = Offer.objects.all().count() + amount_of_deleted_offers[0]
    users_amount = User.objects.all().count()
    matrix = np.ones((users_amount+1,offers_amount+1))
    bid_list = Bid.objects.all()
    for bid in bid_list:
        bidder_id = bid.bidder.id
        offer_id = bid.offer.id
        if (bidder_id,offer_id) not in s:
            matrix[bidder_id][offer_id] += bid_bonus
            s.add((bidder_id,offer_id))

    # need to update matrix every time a user adds something to favourites!!
    users = User.objects.all()
    for user in users:
        fav_offers = Offer.objects.filter(favorites=user)
        for fav_offer in fav_offers:
            matrix[user.id][fav_offer.id] += fav_bonus

    matrix_df = pd.DataFrame(matrix)
    last_updated = timezone.now()
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
        if (bid.bidder.id,bid.offer.id) not in s:
            matrix_df[bid.offer.id][bid.bidder.id] += bid_bonus #first [] should hold COLUMN INDEX and second ROW INDEX
            s.add((bid.bidder.id,bid.offer.id))

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
    try:
        update_users_offers_bids_in_matrix()
    except:
        return
    try:
        if is_add:
            matrix_df[offer_id][user_id] += fav_bonus
        else:
            matrix_df[offer_id][user_id] -= fav_bonus
    except:
        pass


def update_user_offer_matrix():
    # while true
    # filters offers, users, and bids made after a certain date, save user clicks dict into file
    while True:
        save_click_dict()
        update_users_offers_bids_in_matrix()
        sleep(5)


def construct_cos_similar_matrix(): #this can probably be done more efficiently
    global matrix_df
    global co_sim_matrix
    co_sim_matrix = pd.DataFrame(np.ones((len(matrix_df), len(matrix_df))))
    for i in range(1,len(matrix_df)):
        for j in range(1,len(matrix_df)):
            co_sim_matrix[j][i] = 1 - spatial.distance.cosine(matrix_df.iloc[i].tolist(), matrix_df.iloc[j].tolist())
            #co_sim_matrix[j][i] = 1 - spatial.distance.cosine(matrix_df.iloc[i].tolist()[1:], matrix_df.iloc[j].tolist()[1:]) #this is ignoring dummy user and offer.

    #co_sim_matrix = sklearn.metrics.pairwise.cosine_similarity(matrix_df)
    return co_sim_matrix


def calc_weighted_score(user,offer):
    global co_sim_matrix
    global matrix_df
    global prediction_matrix
    # j is the offer
    # i is the user
    numerator = 0.0
    denominator = 0.0
    for i in range(1,len(co_sim_matrix)): # go over all users
        if matrix_df[offer][i] != 1:
            numerator += co_sim_matrix[user][i] * get_real_user_love_for_offer(i,offer)
            denominator += co_sim_matrix[user][i] # this might have to go inside the if!!!!
            # im putting it outside because currently our "like function" is really dumb, taking into considration only if a offer was bidded or not.
        numerator -= co_sim_matrix[user][i]/5 # might have to delete this when i have a better like function, watch this: https://www.youtube.com/watch?v=Fmtorg_dmM0&ab_channel=ritvikmath
        
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
    for i in range(1,len(prediction_matrix)):
        for j in range(1,len(prediction_matrix.iloc[0])):
            prediction_matrix[j][i] = calc_weighted_score(i,j)

def construct_all_matrices():
    if len(matrix_df) >= 1:
        construct_cos_similar_matrix()
        construct_prediction_matrix()

def update_prediction_and_cos_matrices():
    while True:
        construct_all_matrices()
        sleep(1)


def matrices_handler_thread():
    global matrix_df
    global last_updated
    read_click_dict()
    matrix_df = init_matrix()
    last_updated = timezone.now()
    user_offer_update_thread = threading.Thread(target=update_user_offer_matrix, name='user_offer_update_thread', daemon=True)
    user_offer_update_thread.start()

    prediction_and_cos_matrices_thread = threading.Thread(target=update_prediction_and_cos_matrices, name='update_prediction_and_cos_matrices',daemon=True)
    prediction_and_cos_matrices_thread.start()