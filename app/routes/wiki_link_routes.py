from flask import Blueprint, request, jsonify
from app.services.wiki_link_service import get_wikidata_info, get_wikipedia_summary

wiki_link_bp = Blueprint('wiki_link', __name__)


@wiki_link_bp.route('/api/v1/wiki_link', methods=['POST'])
def get_info():
    data = request.get_json()
    iri = data.get("iri")
    if not iri:
        return jsonify({"error": "Missing 'iri' parameter"}), 400

    logo_url, wikipedia_url, error = get_wikidata_info(iri)
    if error:
        return jsonify({"error": error}), 400

    description, wikipedia_url = get_wikipedia_summary(wikipedia_url)

    return jsonify({
        "ontology_iri": iri,
        "wikidata_uri": wikipedia_url,
        "wikipedia_url": wikipedia_url,
        "logo_url": logo_url,
        "description": description
    })
