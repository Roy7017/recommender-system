from datetime import datetime
from threading import Timer
import time
from typing import Dict, List
import pandas as pd
from recommenders.als import ImplicitAlternatingLeastSquares
from recommenders.content_based import ContentBasedRecommender
from recommenders.popularity import PopularityModel
from recommenders.knn import SurpriseKnnNormalModel
from data.interaction_manager import InteractionManager
from data.history_manager import HistoryManager
from item_graph import ItemGraph


class RecommendationEngine:

    # als_model: ImplicitAlternatingLeastSquares
    # content_based_model: ContentBasedRecommender
    # popularity_model: PopularityModel
    # item_knn_model: SurpriseKnnNormalModel
    # prediction_weights: Dict
    # min_service_count: int

    def __init__(
        self,
        als_model: ImplicitAlternatingLeastSquares,
        content_based_model: ContentBasedRecommender,
        popularity_model: PopularityModel,
        item_knn_model: SurpriseKnnNormalModel,
        item_graph: ItemGraph,
        min_service_count: int = 15,
        prediction_weights: Dict = {"als": 0.5, "knn": 0.2, "content": 0.2, "popularity": 0.1},
    ) -> None:
        self.als_model = als_model
        self.content_based_model = content_based_model
        self.popularity_model = popularity_model
        self.item_knn_model = item_knn_model
        self.prediction_weights = prediction_weights
        self.min_service_count = min_service_count

    def train(self):
        users = InteractionManager.get_users()
        user_df = pd.DataFrame.from_records(users)

        services = InteractionManager.get_services()
        self.service_df = pd.DataFrame.from_records(services)

        subscriptions = InteractionManager.get_subscriptions()
        service_subscripted_df = pd.DataFrame.from_records(subscriptions)

        service_subscripted_df["createdAt"] = pd.to_datetime(service_subscripted_df["createdAt"])
        service_subscripted_df = service_subscripted_df.sort_values(by="createdAt")

        train_subscribe_count = service_subscripted_df.groupby(["user", "service"], as_index=False).size()

        self.train_data = train_subscribe_count[["user", "service", "size"]].join(
            self.service_df.set_index("objectId"),
            on="service",
            how="left",
        )

        self.users = self.train_data["user"].unique()
        self.services = self.train_data["service"].unique()

        start = time.time()
        self.als_model.fit(train_data=self.train_data)
        self.item_knn_model.fit(train_data=self.train_data)
        self.content_based_model.fit(train_data=self.train_data, service_data=self.service_df, ngram_range=(1, 3))
        end = time.time()

        metrics = {}  # TODO : Evaluate recommender metrics

        duration = end - start
        date = datetime.now()

        HistoryManager.add_training_event(duration=duration, data=date, metrics=metrics)

    def predict(self):
        global_rankings: Dict[str, List] = {}

        start = time.time()

        global_rankings = self.get_user_rankings()

        # Filter out the services the user has already purchased.
        for user in self.users:
            user_services = self.train_data[self.train_data["user"] == user]["service"].values
            for service in user_services:
                if service in global_rankings[user]:
                    global_rankings[user].remove(service)

        end = time.time()
        duration = end - start
        date = datetime.now()

        recommendation_event = HistoryManager.add_recommendation_event(duration=duration, date=date)
        for user in self.users:
            recommendations = HistoryManager.add_recommendations(recommendation_event.id, user, global_rankings[user])

        return global_rankings

    def get_user_rankings(self):
        global_rankings: Dict[str, List] = {}
        als_rankings: Dict[str, List] = self.als_model.rank_items()
        content_based_rankings = self.content_based_model.rank_items()
        item_knn_rankings = self.item_knn_model.rank_items()
        popularity_rankings = self.popularity_model.rank_items()

        for user in self.users:
            ranks: List[List] = []
            # Check the number of services bought
            # if the number of services bought is less than the minimum defined, we just use the popularity
            # and go to the next user
            user_services = self.train_data[self.train_data["user"] == user]["service"].values
            if len(user_services) < self.min_service_count:
                global_rankings[user] = popularity_rankings[user]
                continue

            for service in self.services:
                als_rank = self.getIndex(als_rankings[user], service)
                content_based_rank = self.getIndex(content_based_rankings[user], service)
                item_knn_rank = self.getIndex(item_knn_rankings[user], service)
                popularity_rank = self.getIndex(popularity_rankings[user], service)

                rank = (
                    als_rank * self.prediction_weights["als"]
                    + content_based_rank * self.prediction_weights["content"]
                    + item_knn_rank * self.prediction_weights["knn"]
                    + popularity_rank * self.prediction_weights["popularity"]
                )
                ranks.append([service, rank])

            ranks.sort(key=lambda item: item[1], reverse=False)
            global_rankings[user] = [rank[0] for rank in ranks]

        return global_rankings

    def get_similar_items(self, item_id):
        return self.als_model.similar_items(item_id)

    def getIndex(self, array: list, item):
        array = list(array)
        if item in array:
            return array.index(item)
        else:
            array.append(item)
            return array.index(item)
