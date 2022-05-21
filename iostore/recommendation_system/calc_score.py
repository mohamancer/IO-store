import pandas as pd
from scipy import sparse
import numpy as np
from offer.models import Offer

# def two_col_data_frame_to_list_of_tuples(user_ratings):
#     records = user_ratings.to_records(index=False)
#     intermediate_result = list(records)
#     result = []
#     for i,tup in enumerate(intermediate_result):
#         result.append((i,tup[0]))
#     return result

# def get_highest_rated_offers(user_ratings , matrix_df):
#     def standardize(row):
#         if row.max() - row.min() != 0:
#             new_row = (row - row.mean())/(row.max()-row.min())
#         else:
#             new_row = row - row.mean()
#         return new_row
    
#     def get_score(movie_name,rating):
#         score = corrMatrix[movie_name]*(rating)
#         score = score.sort_values(ascending=False)
#         return score
    
#     ratings=matrix_df
#     ratings.fillna(0, inplace=True)
#     df_std = ratings.apply(standardize).T

#     sparse_df = sparse.csr_matrix(df_std.values)
#     corrMatrix = pd.DataFrame(cosine_similarity(sparse_df),index=ratings.columns,columns=ratings.columns)

#     corrMatrix = ratings.corr(method='pearson')

#     user_ratings = two_col_data_frame_to_list_of_tuples(pd.DataFrame(user_ratings))
#     result = pd.DataFrame()
#     print(result)

#     for offer_id,rating in user_ratings:
#         #result = pd.concat([result,get_score(offer_id,rating)],axis = 1)
#         result = result.append(get_score(offer_id,rating),ignore_index = True)
#         print(result)

#     print(result)
#     result = result.sum().sort_values(ascending=False)
#     result = result.index
#     result += 1
#     result = result.tolist()
#     return result




# i used this last!
# def get_highest_rated_offers(user_ratings , matrix_df): # user_ratings is list of tuples (offer_id,rating)
#     def standardize(row):
#         if row.max() - row.min() != 0:
#             new_row = (row - row.mean()) / (row.max() - row.min())
#             return new_row
#         return row

#     def calc_intermediate_score(offer_id,rating):
#         #working
#         #print(item_similarity_df[offer_id])
#         score = item_similarity_df[offer_id]*(rating)
#         score = score.sort_values(ascending=False)
#         return score

#     ratings = matrix_df
#     ratings = ratings.fillna(0)

#     ratings_std = ratings.apply(standardize)

#     sparse_df = sparse.csr_matrix(ratings_std.values)
#     item_similarity = cosine_similarity(ratings_std.values) # do i need transpose? (ratings_std.T)

#     item_similarity_df = pd.DataFrame(cosine_similarity(sparse_df.T),index=ratings.columns,columns=ratings.columns)
#     #item_similarity_df = pd.DataFrame(item_similarity, index=ratings_std.columns)

#     result = pd.DataFrame()
#     # print(user_ratings.shape)
#     # for offer_id,rating in user_ratings:
#     #     result = result.append(calc_intermediate_score(offer_id, rating),ignore_index=True)
    
#     user_ratings = two_col_data_frame_to_list_of_tuples(pd.DataFrame(user_ratings))
#     print(user_ratings)
#     for offer_id,rating in user_ratings:
#         result = result.append(calc_intermediate_score(offer_id, rating),ignore_index=True)
#     result = result.sum().sort_values(ascending=False)
#     result = result.index
#     result += 1
#     result = result.tolist()
#     print(matrix_df)
#     print(result)
#     return result
    

def clean_inactive_users(offers):
    active_offers = []
    for offer in offers:
        if offer.active:
            active_offers.append(offer)
    return active_offers

def get_recommanded_offers_ids(user_id):
    from .update_score_matrix import prediction_matrix
    if user_id > len(prediction_matrix): # if the user is a new one, and we didnt add him to the user-offer matrix yet
        return [(i+1) for i in range(len(Offer.objects.all()))][::-1]

    index = user_id - 1
    dic = dict()
    i = 1
    # print(prediction_matrix)
    # print(prediction_matrix.iloc[index].values.tolist())
    for value in prediction_matrix.iloc[index].values:
        if value not in dic:
            dic[value] = [i]
        else:
            dic[value].append(i)
        i+=1
    
    key_list = sorted(dic.keys())
    res = []
    for key in key_list:
        a = dic[key]
        for b in a:
            res.append(b)
    res = res[::-1]
    return res

def get_recommanded_offers(user_id):
    best_match_ids = get_recommanded_offers_ids(user_id)
    offers = []
    for offer_id in best_match_ids:
        offers.append(Offer.objects.get(id = offer_id))
    offers = clean_inactive_users(offers)
    return offers
