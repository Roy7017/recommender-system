import surprise
import pandas as pd
import numpy as np
from typing import Dict

class SurpriseKnnNormalModel(surprise.KNNWithZScore):
    def rank_items(self, users: list, items: list):
        rankings: Dict[str, list] = {}
        for user in users:
            ranking_list = [self.predict(user, item, clip=False) for item in items]
            rankings_df = pd.DataFrame({
                'item': items,
                'ranking': ranking_list
            })
            rankings[user] = rankings_df.sort_values(by='ranking')['item'].values
        return rankings