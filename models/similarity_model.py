from models.interaction_models import Service
from database import db

class ItemSimilarities(db.Document):
    # id = db.StringField(primary_key=True)

    collaborative_sim = db.DecimalField()
    matrix_sim = db.DecimalField()
    content_sim = db.DecimalField()

    service1 = db.LazyReferenceField(Service)
    service2 = db.LazyReferenceField(Service)