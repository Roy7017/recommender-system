from models.feedback_model import Impression

class FeedbackManager():
    @classmethod
    def add_impression(cls, user_id, service_id, date):
        impression = Impression(
            impression_date = date,
            clicked = False,
            user = str(user_id),
            service = str(service_id)
        )
        return impression.save()

    @staticmethod
    def register_click(cls, impression_id):
        impression_id = Impression.objects.get(id=impression_id)
        impression_id.clicked = True
        return impression_id.save()