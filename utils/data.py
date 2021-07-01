from datetime import datetime
import json
import pandas as pd
from models.interaction_models import User, Service, Subscription


def load_data():
    print('\nImporting data...')
    path = "D:\\Projects\\recommender-system\\utils\\columns_removed\\"
    user_df = pd.read_csv(path+"users.csv", index_col="Unnamed: 0")

    service_subscripted_df = pd.read_csv(path+"service_subscripted.csv", index_col="Unnamed: 0")
    service_subscripted_mode_df = pd.read_csv(path+"service_subscripted_modes.csv", index_col="Unnamed: 0")
    service_subscripted_status_df = pd.read_csv(path+"service_subscripted_status.csv", index_col="Unnamed: 0")

    service_df = pd.read_csv(path+"services.csv", index_col="Unnamed: 0")
    service_category_df = pd.read_csv(path+"service_categories.csv", index_col="Unnamed: 0")
    service_class_df = pd.read_csv(path+"service_classes.csv", index_col="Unnamed: 0")
    service_price_df = pd.read_csv(path+"service_prices.csv", index_col="Unnamed: 0")

    service_subscripted_df["user"] = service_subscripted_df["user"].apply(getObjectId)
    service_subscripted_df["service"] = service_subscripted_df["service"].apply(getObjectId)
    service_subscripted_df["servicePrice"] = service_subscripted_df["servicePrice"].apply(getObjectId)
    service_subscripted_df["serviceSubscriptedStatus"] = service_subscripted_df["serviceSubscriptedStatus"].apply(getObjectId)

    service_df["servicePrices"] = service_df["servicePrices"].apply(getObjectIds)
    service_df["serviceCategories"] = service_df["serviceCategories"].apply(getObjectIds)

    user_df.apply(saveUser, axis=1)
    service_df.apply(saveService, axis=1)
    service_subscripted_df.apply(saveSubscription, axis=1)
    print('\nImporting finished.\n')

def getObjectId(string):
    return (
        json.loads(string.replace("'", '"'))["objectId"]
        if type(string) == str
        else None
    )

def getObjectIds(strings):
    strings = json.loads(strings.replace("'", '"')) if type(strings) == str else None
    return [string["objectId"] for string in strings] if not strings is None else None

def saveUser(row):
    user = User(
        id=row['objectId'],
        username=str(row['username']),
        email=str(row['email']),
        last_name=str(row['lastname']),
        mobile=str(row['mobile']),
        city=str(row['city']),
        country=str(row['country'])
    )
    user.save()

def saveService(row):
    service = Service(
        id=row['objectId'],
        name=str(row['name']),
        task_name=str(row['task_name']),
        description=str(row['description']),
        haveAndroidApp=str(row['haveAndroidApp']),
        haveIOSApp=str(row['haveIOSApp'])
    )

    service.save()

def saveSubscription(row):
    subscription = Subscription(
        id=row['objectId'],
        name=str(row['name']),
        url=str(row['url']),
        expired_date=str(row['expired_date']),
        subscription_date=str(row['createdAt']),
        user=str(row['user']),
        service=str(row['service'])
    )
    subscription.save()