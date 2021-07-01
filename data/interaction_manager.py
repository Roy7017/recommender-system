from models.interaction_models import User, Service, Subscription

class InteractionManager():
    @classmethod
    def add_user(cls, user):
        new_user = User(
            id=user['objectId'],
            username=str(user['username']),
            email=str(user['email']),
            last_name=str(user['lastname']),
            mobile=str(user['mobile']),
            city=str(user['city']),
            country=str(user['country'])
        )
        return new_user.save()

    @classmethod
    def modify_user(cls, user_id, user):
        new_user = User.objects.get(id=user_id)
        if user['username'] is not None: new_user.username=str(user['username'])
        if user['email'] is not None: new_user.email=str(user['email'])
        if user['lastname'] is not None: new_user.last_name=str(user['lastname'])
        if user['mobile'] is not None: new_user.mobile=str(user['mobile'])
        if user['city'] is not None: new_user.city=str(user['city'])
        if user['country'] is not None: new_user.country=str(user['country'])
        return new_user.save()

    @classmethod
    def delete_user(cls, user_id):
        user = User.objects.get(id=user_id)
        return user.delete()

    @classmethod
    def add_service(cls, service):
        new_service = Service(
            id=service['objectId'],
            name=str(service['name']),
            task_name=str(service['task_name']),
            description=str(service['description']),
            haveAndroidApp=str(service['haveAndroidApp']),
            haveIOSApp=str(service['haveIOSApp'])
        )

        return new_service.save()

    @classmethod
    def modify_service(cls, service_id, service):
        new_service = Service.objects.get(id=service_id)
        if service['name'] is not None: new_service.name=str(service['name'])
        if service['task_name'] is not None: new_service.task_name=str(service['task_name'])
        if service['description'] is not None: new_service.description=str(service['description'])
        if service['haveAndroidApp'] is not None: new_service.haveAndroidApp=str(service['haveAndroidApp'])
        if service['haveIOSApp'] is not None: new_service.haveIOSApp=str(service['haveIOSApp'])
        return new_service.save()

    @classmethod
    def delete_service(cls, service_id):
        service = Service.objects.get(id=service_id)
        return service.delete()

    @classmethod
    def add_subscription(cls, subscription):
        new_subscription = Subscription(
            id=subscription['objectId'],
            name=str(subscription['name']),
            url=str(subscription['url']),
            expired_date=str(subscription['expired_date']),
            subscription_date=str(subscription['createdAt']),
            user=str(subscription['user']),
            service=str(subscription['service'])
        )
        return new_subscription.save()

    @classmethod
    def modify_subscription(cls, subscription_id, subscription):
        new_subscription = Subscription.objects.get(id=subscription_id)
        if subscription['name'] is not None: new_subscription.name = str(subscription['name'])
        if subscription['url'] is not None: new_subscription.url = str(subscription['url'])
        if subscription['expired_date'] is not None: new_subscription.expired_date = str(subscription['expired_date'])
        if subscription['createdAt'] is not None: new_subscription.subscription_date = str(subscription['createdAt'])
        if subscription['user'] is not None: new_subscription.user = str(subscription['user'])
        if subscription['service'] is not None: new_subscription.service = str(subscription['service'])

        return new_subscription.save()

    @classmethod
    def delete_subscription(cls, subscription_id):
        subscription = Subscription.objects.get(id=subscription_id)
        return subscription.delete()