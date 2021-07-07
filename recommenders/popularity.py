from typing import Dict
from recommenders.base import BaseModel

class PopularityModel(BaseModel):
    def rank_items(self):
        users = self.train_count['user'].unique()
        global_item_count = self.train_count.groupby(by='service', as_index=False).sum().sort_values(by='size', ascending=False)
        rankings: Dict[str, list] = {}
        for user in users:
            rankings[user] = global_item_count['service'].values
        self.rankings = rankings
        return rankings  

    def evaluate_rank(self, N: int=40):
        return super().evaluate_rank(self.rankings, on_train=True, N=N)