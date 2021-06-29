from typing import Dict
import numpy as np
import pandas as pd

def recall_at_N(rankings: Dict[str, list], test_count: pd.DataFrame, N: int = 20):
    recall_sum = 0
    for user in rankings.keys():
        recommendations = rankings[user][:N] # We get the first N items from the ranked list
        relevant_items: list = test_count[test_count['user'] == user].sort_values(by='size', ascending=False)['service'].values
        relevant_recommendations = list(set(recommendations) & set(relevant_items))
        recall = len(relevant_recommendations)/len(relevant_items)
        recall_sum += recall

    mean_recall = recall_sum / len(rankings.keys())
    return mean_recall * 100

def rank_score(rankings: Dict[str, list], test_count: pd.DataFrame, N: int = 20):
    rank_sum = 0
    rating_sum = 0
    for user in rankings.keys():
        # print(len(rankings[user]))
        for (index, item) in enumerate(rankings[user]):
            if(index >= N): break
            rank_ui:float =  (index / len(rankings[user])) * 100
            rating_ui:int = test_count[(test_count['user'] == user) & (test_count['service'] == item)]['size'].values
            if(len(rating_ui) <= 0): rating_ui = 0
            else: rating_ui = rating_ui[0]
            rank_sum += rank_ui*rating_ui
            rating_sum += rating_ui

    expected_rank = rank_sum/rating_sum
    return expected_rank