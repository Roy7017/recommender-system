from models.similarity_model import ItemSimilarities

class SimilarityManager():

    @staticmethod
    def add_similarities(cls, service1_id, service2_id, collaborative_sim, matrix_sim, content_sim):
        # TODO: Handle the case where the pair (service1, service2) or (service2, service1) exist already.

        itemSimilarities = ItemSimilarities(
            collaborative_sim=collaborative_sim,
            matrix_sim=matrix_sim,
            content_sim=content_sim,
            service1=service1_id,
            service2=service2_id
        )
        return itemSimilarities.save()

    @staticmethod
    def get_similarities(cls, service1_id, service2_id):
        service1 = ItemSimilarities.objects(service1 = service1_id, service2=service2_id)