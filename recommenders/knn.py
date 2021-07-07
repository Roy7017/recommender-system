import surprise
import pandas as pd
from typing import Dict
from evaluation import rank_score

class SurpriseKnnNormalModel(surprise.KNNWithZScore):
    def __init__(self, k=40, min_k=1, verbose=True, sim_options={"name": "pearson_baseline", "user_based": False} ,**kwargs):
        super().__init__(k=k, min_k=min_k, sim_options=sim_options, verbose=verbose, **kwargs)

    def fit(self, train_data: pd.DataFrame):
        self.train_data = train_data.copy()

        self.users = self.train_data["user"].unique()
        self.services = self.train_data["service"].unique()

        self.reader = surprise.Reader(rating_scale=(0, self.train_data['size'].max()))
        self.train_dataset = surprise.Dataset.load_from_df(
            self.train_data[["user", "service", "size"]], self.reader
        )

        return super().fit(trainset=self.train_dataset.build_full_trainset())

    def rank_items(self):
        users = self.users
        items = self.services

        rankings: Dict[str, list] = {}
        for user in users:
            ranking_list = [self.predict(user, item, clip=False) for item in items]
            rankings_df = pd.DataFrame({
                'item': items,
                'ranking': ranking_list
            })
            rankings[user] = rankings_df.sort_values(by='ranking')['item'].values

        self.rankings = rankings
        return rankings

    def evaluate_rank(self, N=40):
        return rank_score(rankings=self.rankings, test_count=self.train_data, N=N)