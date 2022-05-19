import pandas as pd
import numpy as np
from scipy import sparse
from sklearn.metrics.pairwise import cosine_similarity
from offer.models import Offer, Bid, User

def get_highest_rated_offers(user_ratings , matrix_df): # user_ratings is list of tuples (offer_id,rating)
    def standardize(row):
        if row.max() - row.min() != 0:
            new_row = (row - row.mean()) / (row.max() - row.min())
            return new_row
        return row

    def calc_intermediate_score(offer_id,rating):
        #working
        score = item_similarity_df[offer_id]*(rating-2.5)
        score = score.sort_values(ascending=False)
        return score

    def clean_list(): # this function takes a list of most movies and removes inactive ones
        "TODO implement this(if needed??)"
        pass

    ratings = matrix_df

    ratings = ratings.fillna(0)
    ratings_std = ratings.apply(standardize)
    item_similarity = cosine_similarity(ratings_std) # do i need transpose? (ratings_std.T)
    item_similarity_df = pd.DataFrame(item_similarity, index=ratings_std.columns)
    
    result = pd.DataFrame()

    for offer_id,rating in user_ratings:
        result = result.append(calc_intermediate_score(offer_id, rating),ignore_index=True)
    
    result = result.sum().sort_values(ascending=False)
    return result
    

