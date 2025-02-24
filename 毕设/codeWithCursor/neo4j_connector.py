from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

load_dotenv()

class Neo4jConnector:
    def __init__(self):
        self.driver = GraphDatabase.driver(
            os.getenv("NEO4J_URI"),
            auth=(
                os.getenv("NEO4J_USER"),
                os.getenv("NEO4J_PASSWORD")
            )
        )
    
    def create_knowledge_graph(self, data):
        """使用UNWIND批量操作优化"""
        with self.driver.session() as session:
            # 批量创建实体
            session.execute_write(
                self._batch_create_entities, 
                data['entities']
            )
            # 批量创建关系
            session.execute_write(
                self._batch_create_relationships,
                data['relationships']
            )
    
    @staticmethod
    def _batch_create_entities(tx, entities):
        query = """
        UNWIND $entities AS entity
        MERGE (e:Entity {name: entity})
        """
        tx.run(query, entities=entities)
    
    @staticmethod
    def _batch_create_relationships(tx, relationships):
        query = """
        UNWIND $rels AS rel
        MATCH (a:Entity {name: rel.source}), (b:Entity {name: rel.target})
        MERGE (a)-[r:RELATION {type: rel.type}]->(b)
        """
        tx.run(query, rels=relationships)
    
    def close(self):
        self.driver.close() 