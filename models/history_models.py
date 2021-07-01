from models.interaction_models import User
from database import db

class RecommendationHistory(db.Document):
    id = db.StringField(primary_key=True)
    duration = db.StringField()
    date = db.StringField()

class Recommendations(db.Document):
    id = db.StringField(primary_key=True)
    items = db.StringField()

    user = db.LazyReferenceField(User)
    recommendation_history = db.LazyReferenceField(RecommendationHistory)

class TrainingHistory(db.Document):
    id = db.StringField(primary_key=True)
    duration = db.StringField()
    date = db.StringField()

    global_mpr = db.DecimalField()
    global_recall = db.DecimalField()

    content_mpr = db.DecimalField()
    content_recall = db.DecimalField()

    matrix_mpr = db.DecimalField()
    matrix_recall = db.DecimalField()

    collaborative_mpr = db.DecimalField()
    collaborative_recall = db.DecimalField()
