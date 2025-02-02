from flask import Blueprint, request, jsonify
from app.services.wiki_link_service import get_wikidata_info, get_wikipedia_summary
from flasgger import swag_from

wiki_link_bp = Blueprint('wiki_link', __name__)


@wiki_link_bp.route('/api/v1/wiki_link', methods=['POST'])
@swag_from({
    "tags": ["Wiki Data Lookup"],
    "summary": "Fetches Wikidata and Wikipedia information for a given ontology entity.",
    "description": "Retrieves the Wikipedia URL, Wikidata URI, logo, and a brief description for a given ontology entity.",
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "iri": {
                        "type": "string",
                        "example": "http://www.semanticweb.org/ana/ontologies/2024/10/JobHunterOntology#.NET",
                        "description": "IRI of the ontology entity for which Wikidata and Wikipedia information is retrieved."
                    }
                }
            }
        }
    ],
    "responses": {
        200: {
            "description": "Successfully retrieved Wikidata and Wikipedia information.",
            "schema": {
                "type": "object",
                "properties": {
                    "ontology_iri": {
                        "type": "string",
                        "example": "http://www.semanticweb.org/ana/ontologies/2024/10/JobHunterOntology#.NET",
                        "description": "IRI of the ontology entity."
                    },
                    "wikipedia_url": {
                        "type": "string",
                        "example": "https://en.wikipedia.org/wiki/.NET",
                        "description": "Wikipedia page URL related to the entity."
                    },
                    "logo_url": {
                        "type": "string",
                        "example": "http://commons.wikimedia.org/wiki/Special:FilePath/Microsoft%20.NET%20logo.svg",
                        "description": "URL of the entity's logo from Wikidata."
                    },
                    "description": {
                        "type": "string",
                        "example": "The .NET platform is a free and open-source, managed computer software framework for Windows, Linux, and macOS operating systems. The project is mainly developed by Microsoft employees by way of the .NET Foundation and is released under an MIT License.",
                        "description": "Brief summary of the entity extracted from Wikipedia."
                    }
                }
            }
        },
        400: {
            "description": "Invalid request, missing 'iri' parameter.",
            "schema": {
                "type": "object",
                "properties": {
                    "error": {
                        "type": "string",
                        "example": "Missing 'iri' parameter"
                    }
                }
            }
        }
    }
})
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
        "wikipedia_url": wikipedia_url,
        "logo_url": logo_url,
        "description": description
    })
