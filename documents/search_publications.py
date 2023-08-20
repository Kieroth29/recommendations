from decouple import config
from lingua import Language, LanguageDetector, LanguageDetectorBuilder
from scholarly import ProxyGenerator, scholarly
from typing import List

from models.recommendation import Recommendation
from storage.cache import Cache
from storage.db import DB

languages = [Language.PORTUGUESE, Language.ENGLISH]


def get_publication_in_desired_languages(pubs, language_detector: LanguageDetector) -> None:
    while True:
        pub = next(pubs)
        if language_detector.detect_language_of(pub["bib"]["title"]) in languages:
            return pub


def get_recommendations(content_list: List[str]) -> List[Recommendation]:
    cache = Cache()
    db = DB()
    recommendations = []
    language_detector = LanguageDetectorBuilder.from_languages(
        *languages).build()

    for content in content_list:
        pubs = scholarly.search_pubs(content, sort_by="date")
        top_pub = get_publication_in_desired_languages(pubs, language_detector)

        recommendation = {
            "title": top_pub["bib"]["title"],
            "venue": top_pub["bib"]["venue"],
            "authors": top_pub["bib"]["author"],
            "url": top_pub["pub_url"],
            "pub_year": top_pub["bib"]["pub_year"]
        }        

        try:
            cache.set_recommendation(recommendation)
        except:
            pass

        try:
            db.insert_recommendation(recommendation)
        except:
            pass

        recommendations.append(recommendation)

    return recommendations
