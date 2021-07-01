from flask import Flask
from flask_cors import CORS
from flask_mongoengine import MongoEngine
from flask_migrate import Migrate

app = Flask(__name__)
CORS(app)

# app.config['CORS_HEADERS'] = 'Content-Type'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mongodb+srv://mutia:<mutia>@cluster0.d7szd.mongodb.net/recommender?retryWrites=true&w=majority'
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# app.config['MONGOALCHEMY_DATABASE'] = 'recommender'
# app.config['MONGOALCHEMY_SERVER'] = 'cluster0.d7szd.mongodb.net'
# app.config['MONGOALCHEMY_USER'] = 'mutia'
app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb+srv://recommender:recommender@cluster0.d7szd.mongodb.net/recommender?authSource=admin&retryWrites=true&w=majority',

    'connect': False,
}

db = MongoEngine(app)
migrate = Migrate(app, db)