from database import db

class User(db.Document):
    id = db.StringField(primary_key=True)
    username = db.StringField()
    email = db.StringField()
    last_name = db.StringField()
    mobile = db.StringField()
    city = db.StringField()
    country = db.StringField()

class Service(db.Document):
    id = db.StringField(primary_key=True)
    name = db.StringField()
    task_name = db.StringField()
    description = db.StringField()
    haveAndroidApp = db.BooleanField()
    haveIOSApp = db.BooleanField()

class Subscription(db.Document):
    id = db.StringField(primary_key=True)
    name = db.StringField()
    url = db.StringField()
    expired_date = db.StringField()
    subscription_date = db.StringField()

    user = db.LazyReferenceField(User)

    service = db.LazyReferenceField(Service)
