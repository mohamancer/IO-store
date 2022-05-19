import pandas as pd
import numpy as np
from scipy import sparse
from sklearn.metrics.pairwise import cosine_similarity
from .models import Offer, Bid, User

def get_highest_rated_offers(user_ratings): # user_ratings is list of tuples (offer_id,rating)
    def standardize(row):
        new_row = (row - row.mean()) / (row.max() - row.min())
        return new_row
    def calc_intermediate_score(movie_name,rating):
        similar_score = item_similarity_df[movie_name]*(rating-2.5)
        similar_score = similar_score.sort_values(ascending=False)
        return similar_score
    

    def clean_list(): # this function takes a list of most movies and removes inactive ones
        pass

    try:
        ratings = pd.read_csv('user_ratings.csv', index_col=0)
    except:
        user_amount = User.objects.all().count()
        offer_amount = Offer.objects.all().count()
        empty_ratings = np.zeroes((user_amount,offer_amount))
        ratings = pd.DataFrame()
        pass

    ratings = ratings.fillna(0)
    ratings_std = ratings.apply(standardize).T
    item_similarity = cosine_similarity(ratings_std)
    item_similarity = cosine_similarity(ratings_std.T)
    sparse_df = sparse.csr_matrix(ratings_std.values)
    item_similarity_df = pd.DataFrame(cosine_similarity(sparse_df),index=ratings.columns,columns=ratings.columns)
    corrMatrix = pd.DataFrame(cosine_similarity(sparse_df),index=ratings.columns,columns=ratings.columns)
    
    result = pd.DataFrame()
    for offer_id,rating in user_ratings:
        result = result.append(calc_intermediate_score(offer_id, rating),ignore_index=True)

    result = result.sum().sort_values(ascending=False)
    
    return result
    

