from typing import Dict
from database import db

class User(db.Document):
    id = db.StringField(primary_key=True)
    username = db.StringField()
    email = db.StringField()
    last_name = db.StringField()
    mobile = db.StringField()
    city = db.StringField()
    country = db.StringField()

    def to_dict(self) -> Dict:
        return {
            'objectId': self.id,
            'username': self.username,
            'email': self.email,
            'lastname': self.last_name,
            'mobile': self.mobile,
            'city': self.city,
            'country': self.country
        }

class Service(db.Document):
    id = db.StringField(primary_key=True)
    name = db.StringField()
    task_name = db.StringField()
    description = db.StringField()
    haveAndroidApp = db.BooleanField()
    haveIOSApp = db.BooleanField()

    def to_dict(self) -> Dict:
        return {
            'objectId': self.id,
            'name': self.name,
            'task_name': self.task_name,
            'description': self.description,
            'haveAndroidApp': self.haveAndroidApp,
            'haveIOSApp': self.haveIOSApp
        }

class Subscription(db.Document):
    id = db.StringField(primary_key=True)
    name = db.StringField()
    url = db.StringField()
    expired_date = db.StringField()
    subscription_date = db.StringField()

    user = db.LazyReferenceField(User)

    service = db.LazyReferenceField(Service)

    def to_dict(self) -> Dict:
        return {
            'objectId': self.id,
            'name': self.name,
            'url': self.url,
            'expired_date': self.expired_date,
            'createdAt': self.subscription_date,
            'user': self.user,
            'service': self.service
        }
