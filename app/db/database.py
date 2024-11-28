from neo4j import GraphDatabase

from app.settings.neo4j_config import *

auth = (NEO4J_USER, NEO4J_PASSWORD)

driver = GraphDatabase.driver(
    NEO4J_URI,
    auth=auth
)
