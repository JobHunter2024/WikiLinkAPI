from SPARQLWrapper import SPARQLWrapper, JSON
import requests
from app.exceptions.exception_handler import BadRequestException

WIKIPEDIA_API_ENDPOINT = "https://en.wikipedia.org/api/rest_v1/page/summary/"
EXTERNAL_SPARQL_API = "http://localhost:8887/api/v1/query"
NAMESPACE = "http://www.semanticweb.org/ana/ontologies/2024/10/JobHunterOntology#"


def generate_wikidata_query(iri):
    return f"""
    SELECT DISTINCT ?wikidataURI WHERE {{
        <{iri}> <http://www.semanticweb.org/ana/ontologies/2024/10/JobHunterOntology#wikidataURI> ?wikidataURI .
    }}
    """


def call_external_api(endpoint, namespace, iri, query):
    """Calls the SPARQL API to fetch entity data."""
    try:
        response = requests.post(endpoint, json={
            "namespace": namespace,
            "query": query(iri)
        }, headers={
            "Accept": "application/sparql-results+json",
            "Content-Type": "application/json"
        })

        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise BadRequestException(f"Failed to fetch data from external API: {str(e)}")


def extract_wikidata_uri(response):
    for result in response.get("resultList", []):
        if "wikidataURI" in result:
            wikidata_uri = result["wikidataURI"]
            if wikidata_uri.startswith('"') and "^^" in wikidata_uri:
                wikidata_uri = wikidata_uri.split("^^")[0].strip('"')
            return wikidata_uri
    return None


def get_wikipedia_summary(wikipedia_url):
    if not wikipedia_url:
        return None, None

    title = wikipedia_url.split("/")[-1]
    url = WIKIPEDIA_API_ENDPOINT + title
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data.get("extract", ""), wikipedia_url
    return None, wikipedia_url


def get_wikidata_info(ontology_iri):
    response = call_external_api(EXTERNAL_SPARQL_API, NAMESPACE, ontology_iri, generate_wikidata_query)
    wikidata_uri = extract_wikidata_uri(response)

    if not wikidata_uri:
        return None, None, "No Wikidata URI found for this entity"

    wikidata_id = wikidata_uri.split("/")[-1]

    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    query = f"""
    SELECT ?logo ?sitelink WHERE {{
      OPTIONAL {{ wd:{wikidata_id} wdt:P154 ?logo. }}  # Fetch logo
      OPTIONAL {{
        ?sitelink schema:about wd:{wikidata_id};
                  schema:isPartOf <https://en.wikipedia.org/>.
      }}  # Fetch Wikipedia link
    }}
    """
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)

    try:
        results = sparql.query().convert()
    except Exception as e:
        return None, None, f"SPARQL query error: {str(e)}"

    logo_url = None
    wikipedia_url = None

    for result in results["results"]["bindings"]:
        if "logo" in result:
            logo_url = result["logo"]["value"]
        if "sitelink" in result:
            wikipedia_url = result["sitelink"]["value"]

    return logo_url, wikipedia_url, None
