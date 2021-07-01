import recommenders
from data.interaction_manager import InteractionManager

class Controller():
    def __init__(self) -> None:
        pass

    def train_recommenders(self):
        pass

    def generate_recommendations(self):
        pass

    def register_click(self, impression_id):
        pass

    def get_recommendations(self, user_id):
        pass

    def get_similar_items(self, item_id):
        pass

    def get_associated_items(self, item_id):
        pass

    def add_user(self, user):
        InteractionManager.add_user(user)

    def modify_user(self, user_id, user):
        InteractionManager.modify_user(user_id, user)

    def delete_user(self, user_id):
        InteractionManager.delete_user(user_id)

    def add_service(self, service):
        InteractionManager.add_service(service)

    def modify_service(self, service_id, service):
        InteractionManager.modify_service(service_id, service)

    def delete_service(self, service_id):
        InteractionManager.delete_service(service_id)

    def add_subscription(self, subscription):
        InteractionManager.add_subscription(subscription)

    def modify_subscription(self, subscription_id, subscription):
        InteractionManager.modify_subscription(subscription_id, subscription)

    def delete_subscription(self, subscription_id):
        InteractionManager.delete_subscription(subscription_id)