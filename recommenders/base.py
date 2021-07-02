import pandas as pd
from typing import Dict

from evaluation import recall_at_N, rank_score


class BaseModel:
    def __init__(self):
        self.train_count = None
        self.rankings = None

    def fit(self, train_data: pd.DataFrame):
        self.train_count = train_data.copy()

    def rank_items(self):
        pass

    def evaluate_recall(self, rankings: Dict[str, list], N: int = 20, on_train: bool = False):
        if rankings is None:
            raise Exception("Rankings cannot be None")
        else:
            return recall_at_N(rankings=rankings, test_count=self.train_count, N=N)

    def evaluate_rank(self, rankings: Dict[str, list], on_train: bool = False, N: int = 20):
        if rankings is None:
            raise Exception("Rankings cannot be None")
        else:
            return rank_score(rankings=rankings, test_count=self.train_count, N=N)
