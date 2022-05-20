import pandas as pd
from scipy import sparse
from sklearn.metrics.pairwise import cosine_similarity

def two_col_data_frame_to_list_of_tuples(user_ratings):
    records = user_ratings.to_records(index=False)
    intermediate_result = list(records)
    result = []
    for i,tup in enumerate(intermediate_result):
        result.append((i,tup[0]))
    return result

def get_highest_rated_offers(user_ratings , matrix_df):
    def standardize(row):
        if row.max() - row.min() != 0:
            new_row = (row - row.mean())/(row.max()-row.min())
        else:
            new_row = row - row.mean()
        return new_row
    
    def get_score(movie_name,rating):
        score = corrMatrix[movie_name]*(rating)
        score = score.sort_values(ascending=False)
        return score
    
    ratings=matrix_df
    ratings.fillna(0, inplace=True)
    df_std = ratings.apply(standardize).T

    sparse_df = sparse.csr_matrix(df_std.values)
    corrMatrix = pd.DataFrame(cosine_similarity(sparse_df),index=ratings.columns,columns=ratings.columns)

    corrMatrix = ratings.corr(method='pearson')

    user_ratings = two_col_data_frame_to_list_of_tuples(pd.DataFrame(user_ratings))
    result = pd.DataFrame()
    for offer_id,rating in user_ratings:
        result = result.append(get_score(offer_id,rating),ignore_index = True)
    result = result.sum().sort_values(ascending=False)
    result = result.index
    result += 1
    result = result.tolist()
    return result

# import pandas as pd
# import numpy as np
# from scipy import sparse
# from sklearn.metrics.pairwise import cosine_similarity
# from offer.models import Offer, Bid, User

# def get_highest_rated_offers(user_ratings , matrix_df): # user_ratings is list of tuples (offer_id,rating)
#     def standardize(row):
#         if row.max() - row.min() != 0:
#             new_row = (row - row.mean()) / (row.max() - row.min())
#             return new_row
#         return row

#     def calc_intermediate_score(offer_id,rating):
#         #working
#         #print(item_similarity_df[offer_id])
#         score = item_similarity_df[offer_id]*(rating-1)
#         score = score.sort_values(ascending=False)
#         return score

#     ratings = matrix_df
#     ratings = ratings.fillna(0)

#     ratings_std = ratings.apply(standardize)

#     sparse_df = sparse.csr_matrix(ratings_std.values)
#     item_similarity_df = pd.DataFrame(cosine_similarity(sparse_df),index=ratings.T.columns,columns=ratings.columns)
#     #item_similarity = cosine_similarity(ratings_std) # do i need transpose? (ratings_std.T)
#     #item_similarity_df = pd.DataFrame(item_similarity, index=ratings_std.columns)

#     result = pd.DataFrame()
#     # print(user_ratings.shape)
#     # for offer_id,rating in user_ratings:
#     #     result = result.append(calc_intermediate_score(offer_id, rating),ignore_index=True)
    
#     i = 0
#     for rating in user_ratings:
#         result = result.append(calc_intermediate_score(i, rating),ignore_index=True)
#         i+=1

#     result = result.sum().sort_values(ascending=False)
#     return result
    

