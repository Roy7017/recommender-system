from models.similarity_model import ItemSimilarities

class SimilarityManager():

    @staticmethod
    def add_or_update_similarities(cls, service1_id, service2_id, collaborative_sim, matrix_sim, content_sim):
        [service1_id, service2_id] = sorted([service1_id, service2_id])

        similarities = ItemSimilarities.objects(service1=service1_id, service2=service2_id)

        if len(similarities) <= 0:
            itemSimilarities = ItemSimilarities(
                collaborative_sim=collaborative_sim,
                matrix_sim=matrix_sim,
                content_sim=content_sim,
                service1=service1_id,
                service2=service2_id
            )
            return itemSimilarities.save()
        else:
            for similarity in similarities:
                similarity.collaborative_sim = collaborative_sim
                similarity.matrix_sim = matrix_sim
                similarity.content_sim = content_sim

    @staticmethod
    def get_similarities(cls, service1_id, service2_id):
        [service1_id, service2_id] = sorted([service1_id, service2_id])
        similarities = ItemSimilarities.objects(service1 = service1_id, service2=service2_id)

        if len(similarities) > 0:
            similarities = similarities.first()
            return {
                'collaborative_sim': similarities.collaborative_sim,
                'matrix_sim': similarities.matrix_sim,
                'content_sim': similarities.content_sim
            }
        else:
            return None