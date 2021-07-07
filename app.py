from recommendation_engine import RecommendationEngine
from recommenders.popularity import PopularityModel
from recommenders.content_based import ContentBasedRecommender
from recommenders.knn import SurpriseKnnNormalModel
from recommenders.als import ImplicitAlternatingLeastSquares
from controller import Controller
from flask import request, abort
from flask_cors import cross_origin
from database import app
from utils.data import load_data

als_model = ImplicitAlternatingLeastSquares(factors=100, regularization=0.1, iterations=1000, alpha=40)
item_knn_model = SurpriseKnnNormalModel()
content_based_model = ContentBasedRecommender()
popularity_model = PopularityModel()

recommendation_engine = RecommendationEngine(
    content_based_model=content_based_model,
    als_model=als_model,
    popularity_model=popularity_model,
    item_knn_model=item_knn_model
)

controller = Controller(
    recommendation_engine=recommendation_engine
)


@app.route("/recommendations/<user_id>", methods=["GET"])
@cross_origin()
def get_recommendations(user_id):
    recommendations = controller.get_recommendations(user_id)
    return {'recommendations': recommendations}


@app.route("/similar-items/<item_id>", methods=["GET"])
@cross_origin()
def get_similar_items(item_id):
    items = controller.get_similar_items(item_id)
    return {'items': items}


@app.route("/associated-items/<item_id>", methods=["GET"])
@cross_origin()
def get_associated_items(item_id):
    # TODO: Implement this
    pass


@app.route("/register-click/<impression_id>", methods=["POST"])
@cross_origin()
def register_click(impression_id):
    is_registered = controller.register_click(impression_id)
    return {'registerd': is_registered}


@app.route("/users", methods=["POST"])
@cross_origin()
def add_user():
    pass


@app.route("/users/<user_id>", methods=["POST"])
@cross_origin()
def modify_user(user_id):
    pass


@app.route("/users/<user_id>", methods=["DELETE"])
@cross_origin()
def delete_user(user_id):
    pass


@app.route("/services", methods=["POST"])
@cross_origin()
def add_service():
    pass


@app.route("/service/<service_id>", methods=["POST"])
@cross_origin()
def modify_service(service_id):
    pass


@app.route("/services/<service_id>", methods=["DELETE"])
@cross_origin()
def delete_service(service_id):
    pass


@app.route("/subscriptions", methods=["POST"])
@cross_origin()
def add_subscription():
    pass


@app.route("/subscription/<subscription_id>", methods=["POST"])
@cross_origin()
def modify_subscription(subscription_id):
    pass


@app.route("/subscriptions/<subscription_id>", methods=["DELETE"])
@cross_origin()
def delete_subscription(subscription_id):
    pass


if __name__ == "__main__":
    app.run(debug=True)
    print("Server started")