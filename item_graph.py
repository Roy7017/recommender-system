import logging
from neo4j import GraphDatabase

class ItemGraph():

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        # Don't forget to close the driver connection when you are finished with it
        self.driver.close()

    @staticmethod
    def _add_service(tx, service_id, name):
        tx.run("MERGE (s:Service {serviceId: $service_id, name: $name}) RETURN s", service_id=service_id, name=name)

    def add_service(self, service_id, name):
        with self.driver.session() as session:
            session.write_transaction(self._add_service, service_id, name)

    @staticmethod
    def _remove_service(tx, service_id):
        tx.run("MATCH (s:Service {serviceId: $service_id}) -[r:WORKS_WITH]- (:Service)"
                "DELETE r"
                "DELETE s", service_id=service_id)

    def remove_service(self, service_id):
        with self.driver.session() as session:
            session.write_transaction(self._remove_service, service_id)

    @staticmethod
    def _remove_association_of(tx, service_id1, service_id2):
        tx.run("MATCH (:Service {serviceId: $service_id1}) -[r:WORKS_WITH]- (:Service {serviceId: $service_id2})"
                "DELETE r", service_id1=service_id1, service_id2=service_id2)

    def remove_association(self, service_id1, service_id2):
        with self.driver.session() as session:
            session.write_transaction(self._remove_association_of, service_id1, service_id2)

    @staticmethod
    def _make_asociation_of(tx, service_id1, service_id2):
        tx.run("MERGE (s1:Service {serviceId: $service_id1})"
                "MERGE (s2:Service {serviceId: $service_id2})"
                "MERGE (s1)-[:WORKS_WITH]-(s2)", service_id1=service_id1, service_id2=service_id2)

    def make_association(self, service_id1, service_id2):
        with self.driver.session() as session:
            session.write_transaction(self._make_asociation_of, service_id1, service_id2)

    @staticmethod
    def _get_associated_items(tx, service_id):
        items = []
        result = tx.run("MATCH (s:Service) -[:WORKS_WITH]- (t:Service {serviceId: $service_id}) RETURN s", service_id=service_id)
        for record in result:
            items.append(record)
        return items

    def get_associated_items(self, service_id):
        with self.driver.session() as session:
            items = session.read_transaction(self._get_associated_items, service_id)
            item_ids = [item['s']['serviceId'] for item in items]
            return item_ids