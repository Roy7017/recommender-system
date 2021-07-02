from models.history_models import TrainingHistory, RecommendationHistory, Recommendations

class HistoryManager():
    @classmethod
    def add_recommendation_event(cls, duration, date):
        new_recommendation_event = RecommendationHistory(
            duration=duration,
            date=date
        )
        return new_recommendation_event.save()

    @classmethod
    def add_recommendations(cls, recommendation_event_id, user_id, recommendations):
        new_recommendations = Recommendations(
            items=recommendations,
            user = user_id,
            recommendation_history=recommendation_event_id
        )
        new_recommendations.save()

    @staticmethod
    def get_recommendations(cls, user_id):
        latest_recommendation_event = RecommendationHistory.objects.order_by('-date').first()
        recommendations = Recommendations.objects(recommendation_history = latest_recommendation_event.id ).first()
        return recommendations.items

    @staticmethod
    def add_training_event(cls, duration, date, metrics):
        new_training_event = TrainingHistory(
            date=date,
            duration=duration
        )

        if metrics['global_mpr'] is not None: new_training_event.global_mpr = float(metrics['global_mpr'])
        if metrics['global_recall'] is not None: new_training_event.global_recall = float(metrics['global_recall'])

        if metrics['content_mpr'] is not None: new_training_event.content_mpr = float(metrics['content_mpr'])
        if metrics['content_recall'] is not None: new_training_event.content_recall = float(metrics['content_recall'])

        if metrics['matrix_mpr'] is not None: new_training_event.matrix_mpr = float(metrics['matrix_mpr'])
        if metrics['matrix_recall'] is not None: new_training_event.matrix_recall = float(metrics['matrix_recall'])

        if metrics['collaborative_mpr'] is not None: new_training_event.collaborative_mpr = float(metrics['collaborative_mpr'])
        if metrics['collaborative_recall'] is not None: new_training_event.collaborative_recall = float(metrics['collaborative_recall'])

        return new_training_event.save()