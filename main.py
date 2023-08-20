import json
from typing import List

from decouple import config
from flask import Flask, request
from PyPDF2 import PdfReader

from documents.generate_documents import export_sheet
from documents.read_syllabus import extract_classes_subjects, get_programatic_content
from documents.search_publications import get_recommendations
from models.publication import Publication
from models.recommendation import Recommendation
from storage.cache import Cache
from storage.db import DB
from utils.responses import success_response_handler, client_error_response_handler, server_error_response_handler
from utils.validators import publication_creation_payload_is_valid
from utils.exceptions import PublicationAlreadyExists


app = Flask(__name__)
cache = Cache()
db = DB()


@app.route("/publication", methods=["POST"])
def create_publication():
    data = request.get_json()

    if not publication_creation_payload_is_valid(data):
        return client_error_response_handler(message="Payload invalid", status=422)

    try:
        cache.set_publication(data)
    except PublicationAlreadyExists:
        return client_error_response_handler(message="Publication already exists", status=409)
    except Exception as e:
        return server_error_response_handler(message=str(e))

    return success_response_handler(json.dumps({"message": "Publication created successfully"}), status=201)


@app.route("/publication", methods=["GET"])
def read_publication():
    data = request.get_json()

    if "title" not in data:
        return client_error_response_handler(message="Publication title not on payload")

    publication = cache.get("publication", data["title"])

    if publication:
        return success_response_handler(publication.model_dump_json(), status=200)

    return client_error_response_handler(message="Publication not found", status=404)


@app.route("/recharge_cache", methods=["POST"])
def recharge_cache():
    publications: List[Publication] = db.find('publication', {})
    recommendations: List[Recommendation] = db.find('recommendation', {})

    cache.set_items_batch(
        'publication', 
        [publication.model_dump() for publication in publications]
    )
    cache.set_items_batch(
        'recommendation', 
        [recommendation.model_dump() for recommendation in recommendations]
    )

    return success_response_handler(json.dumps({"message": "Cache recharged successfully"}), status=200)


@app.route('/generate_recommendations', methods=["POST"])
def generate_recommendations():
    syllabus = request.files['syllabus']

    pdfReader = PdfReader(syllabus)

    programatic_content = []

    for page_number in range(0, len(pdfReader.pages)):
        page = pdfReader.pages[page_number]
        page_text = page.extract_text()

        if "CONTEÚDO PROGRAMÁTICO" in page_text:
            programatic_content = get_programatic_content(page_text)
            break

    extract_classes_subjects(programatic_content)

    recommendations = get_recommendations(programatic_content)
    return success_response_handler(json.dumps({"recommendations": recommendations}), status=200)


if __name__ == "__main__":
    if config("APP_ENVIRONMENT") == "production":
        app.run()
    else:
        app.run(debug=True)
