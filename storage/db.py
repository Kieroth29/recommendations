from typing import Dict, List

from decouple import config
from pymongo import MongoClient
from pymongo.collection import Collection

from models.publication import Publication
from models.recommendation import Recommendation
from utils.exceptions import PublicationAlreadyExists, RecommendationAlreadyExists


class DB():
    def __init__(self) -> None:
        self.client = MongoClient(config('DB_URL'))
        self.db = self.client['recommendations']
        self.recommendations: Collection = self.db.recommendations
        self.publications: Collection = self.db.publications

    def find(self, collection: str, query: Dict) -> List[Dict]:
        if collection == "publication":
            return [Publication(**publication) for publication in self.publications.find(query)]
        elif collection == "recommendation":
            return [Recommendation(**recommendation) for recommendation in self.recommendations.find(query)]

    def insert_publication(self, publication: Publication) -> None:
        if self.get_publication(publication.title):
            raise PublicationAlreadyExists(resource="db")
        self.publications.insert_one(publication.model_dump())

    def get_publication(self, title: str) -> (Dict | None):
        return self.publications.find_one({"title": title})

    def insert_recommendation(self, recommendation: Recommendation) -> None:
        if self.get_recommendation(recommendation.class_topic):
            raise RecommendationAlreadyExists(resource="db")
        self.recommendations.insert_one(recommendation.model_dump())

    def get_recommendation(self, class_topic: str) -> (Dict | None):
        return self.recommendations.find_one({"class_topic": class_topic})
