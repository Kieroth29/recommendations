from lingua import Language, LanguageDetector, LanguageDetectorBuilder
from scholarly import scholarly
from typing import Dict, List, Union
from models.publication import Publication

from models.recommendation import Recommendation
from storage.cache import Cache
from storage.db import DB
from utils.exceptions import PublicationAlreadyExists, RecommendationAlreadyExists

languages = [Language.PORTUGUESE, Language.ENGLISH]
cache = Cache()
db = DB()


def get_publication_in_desired_languages(pubs, language_detector: LanguageDetector) -> Union[Dict, None]:
    while True:
        try:
            pub = next(pubs)
        except StopIteration:
            return None
        
        if language_detector.detect_language_of(pub["bib"]["title"]) in languages:
            return pub


def persist(recommendation: Recommendation, publication: Publication) -> None:
    try:
        cache.set_recommendation(recommendation)
    except RecommendationAlreadyExists:
        pass

    try:
        cache.set_publication(publication)
    except PublicationAlreadyExists:
        pass
    
    try:
        db.insert_recommendation(recommendation)
    except RecommendationAlreadyExists:
        pass
    
    try:
        db.insert_publication(publication)
    except PublicationAlreadyExists:
        pass


def get_recommendations(content_list: List[str]) -> List[Recommendation]:
    recommendations = []
    language_detector = LanguageDetectorBuilder.from_languages(
        *languages).build()

    for content in content_list:
        pubs = scholarly.search_pubs(content, sort_by="date")
        top_pub = get_publication_in_desired_languages(pubs, language_detector)

        if top_pub:
            pub_year = top_pub["bib"]["pub_year"]
            recommendation = Recommendation(**{
                "class_topic": content,
                "title": top_pub["bib"]["title"],
                "venue": top_pub["bib"]["venue"],
                "authors": top_pub["bib"]["author"],
                "url": top_pub["pub_url"],
                "pub_year": int(pub_year) if type(pub_year) == int else None
            })
            
            publication = Publication(**{
                "title": top_pub["bib"]["title"],
                "venue": top_pub["bib"]["venue"],
                "authors": top_pub["bib"]["author"],
                "url": top_pub["pub_url"],
                "num_citations": top_pub["num_citations"],
                "pub_year": int(pub_year) if type(pub_year) == int else None
            })

            persist(recommendation, publication)

            recommendations.append(recommendation.model_dump())

    return recommendations
