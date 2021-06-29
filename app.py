from flask import Flask,request,abort
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from controller import Controller

app = Flask(__name__)
CORS(app)

app.config['CORS_HEADERS'] = 'Content-Type'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/flasksql'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# db = SQLAlchemy(app)
# migrate = Migrate(app, db)

@app.route('/recommendations/<user_id>', methods=['GET'])
@cross_origin()
def get_recommendations(user_id):
    pass

@app.route('/similar-items/<item_id>', methods=['GET'])
@cross_origin()
def get_similar_items(item_id):
    pass

@app.route('/associated-items/<item_id>', methods=['GET'])
@cross_origin()
def get_associated_items(item_id):
    pass

@app.route('/register-click/<impression_id>', methods=['POST'])
@cross_origin()
def register_click(impression_id):
    pass

@app.route('/users', methods=['POST'])
@cross_origin()
def add_user():
    pass

@app.route('/users/<user_id>', methods=['POST'])
@cross_origin()
def modify_user(user_id):
    pass

@app.route('/users/<user_id>', methods=['DELETE'])
@cross_origin()
def delete_user(user_id):
    pass

@app.route('/services', methods=['POST'])
@cross_origin()
def add_service():
    pass

@app.route('/service/<service_id>', methods=['POST'])
@cross_origin()
def modify_service(service_id):
    pass

@app.route('/services/<service_id>', methods=['DELETE'])
@cross_origin()
def delete_service(service_id):
    pass

@app.route('/subscriptions', methods=['POST'])
@cross_origin()
def add_subscription():
    pass

@app.route('/subscription/<subscription_id>', methods=['POST'])
@cross_origin()
def modify_subscription(subscription_id):
    pass

@app.route('/subscriptions/<subscription_id>', methods=['DELETE'])
@cross_origin()
def delete_subscription(subscription_id):
    pass

if __name__=="__main__":
    # db.create_all()
    app.run(debug=True)