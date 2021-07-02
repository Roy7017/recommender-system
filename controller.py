from recommendation_engine import RecommendationEngine
from data.interaction_manager import InteractionManager
from data.feedback_manager import FeedbackManager
from data.history_manager import HistoryManager

class Controller():
    # def __init__(self) -> None:
    #     pass

    @classmethod
    def train_recommenders(cls):
        RecommendationEngine.train()

    @classmethod
    def generate_recommendations(cls):
        RecommendationEngine.predict()

    @classmethod
    def register_click(cls, impression_id):
        FeedbackManager.register_click(impression_id=impression_id)

    @classmethod
    def get_recommendations(cls, user_id, n=40):
        recommendations = HistoryManager.get_recommendations(user_id)[:n]
        return recommendations

    @classmethod
    def get_similar_items(cls, item_id):
        pass

    @classmethod
    def get_associated_items(cls, item_id):
        pass

    @classmethod
    def add_user(cls, user):
        InteractionManager.add_user(user)

    @classmethod
    def modify_user(cls, user_id, user):
        InteractionManager.modify_user(user_id, user)

    @classmethod
    def delete_user(cls, user_id):
        InteractionManager.delete_user(user_id)

    @classmethod
    def add_service(cls, service):
        InteractionManager.add_service(service)

    @classmethod
    def modify_service(cls, service_id, service):
        InteractionManager.modify_service(service_id, service)

    @classmethod
    def delete_service(cls, service_id):
        InteractionManager.delete_service(service_id)

    @classmethod
    def add_subscription(cls, subscription):
        InteractionManager.add_subscription(subscription)

    @classmethod
    def modify_subscription(cls, subscription_id, subscription):
        InteractionManager.modify_subscription(subscription_id, subscription)

    @classmethod
    def delete_subscription(cls, subscription_id):
        InteractionManager.delete_subscription(subscription_id)