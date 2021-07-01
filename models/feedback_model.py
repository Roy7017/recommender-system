from models.interaction_models import Service, User
from database import db

class Impression(db.Document):
    # id = db.StringField(primary_key=True)
    impression_date = db.StringField()
    clicked = db.BooleanField()

    user = db.LazyReferenceField(User)

    service = db.LazyReferenceField(Service)