import json

from decouple import config
from redis import Redis
from typing import Dict, List

from models.publication import Publication
from models.recommendation import Recommendation
from utils.exceptions import PublicationAlreadyExists, RecommendationAlreadyExists


class Cache():
    def __init__(self) -> None:
        self.cache = Redis(host=config('CACHE_HOST'), port=config(
            'CACHE_PORT'), password=config('CACHE_PASS'))

    def get(self, key: str, title: str) -> None | Publication:
        object = self.cache.get(f"{key}:{title}")

        if not object:
            return None

        if key == "publication":
            return Publication(**json.loads(object))
        elif key == "recommendation":
            return Recommendation(**json.loads(object))

    def set_publication(self, publication: Publication) -> None:
        if self.get(publication.title):
            raise PublicationAlreadyExists()

        self.cache.set(
            f"publication:{publication.title}", publication.model_dump_json())

    def set_recommendation(self, recommendation: Recommendation) -> None:
        if self.get(recommendation.title):
            raise RecommendationAlreadyExists()

        self.cache.set(
            f"recommendation:{recommendation.title}", recommendation.model_dump_json())

    def set_items_batch(self, key: str, items: List[Dict]) -> None:
        pipe = self.cache.pipeline()

        for item in items:
            pipe.set(f"{key}:{item['title']}", json.dumps(item))
        pipe.execute()
