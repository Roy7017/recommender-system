from recommendation_engine import RecommendationEngine
from data.interaction_manager import InteractionManager
from data.feedback_manager import FeedbackManager
from data.history_manager import HistoryManager

class Controller():
    def __init__(
        self,
        recommendation_engine: RecommendationEngine
    ) -> None:
        self.recommendation_engine = recommendation_engine

    @classmethod
    def train_recommenders(self):
        self.recommendation_engine.train()

    @classmethod
    def generate_recommendations(self):
        self.recommendation_engine.predict()

    @classmethod
    def register_click(self, impression_id):
        impression = FeedbackManager.register_click(impression_id=impression_id)
        if impression is not None: return True
        else: return False

    @classmethod
    def get_recommendations(self, user_id, n=40):
        recommendations = HistoryManager.get_recommendations(user_id)[:n]
        return recommendations

    @classmethod
    def get_similar_items(self, item_id, n=30):
        return self.recommendation_engine.get_similar_item(item_id)[:n] 

    @classmethod
    def get_associated_items(self, item_id):
        pass

    @classmethod
    def add_user(self, user):
        InteractionManager.add_user(user)

    @classmethod
    def modify_user(self, user_id, user):
        InteractionManager.modify_user(user_id, user)

    @classmethod
    def delete_user(self, user_id):
        InteractionManager.delete_user(user_id)

    @classmethod
    def add_service(self, service):
        InteractionManager.add_service(service)

    @classmethod
    def modify_service(self, service_id, service):
        InteractionManager.modify_service(service_id, service)

    @classmethod
    def delete_service(self, service_id):
        InteractionManager.delete_service(service_id)

    @classmethod
    def add_subscription(self, subscription):
        InteractionManager.add_subscription(subscription)

    @classmethod
    def modify_subscription(self, subscription_id, subscription):
        InteractionManager.modify_subscription(subscription_id, subscription)

    @classmethod
    def delete_subscription(self, subscription_id):
        InteractionManager.delete_subscription(subscription_id)