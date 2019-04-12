from SPARQLWrapper import SPARQLWrapper, JSON

# url where the query has to be sent through the wrapper
sparql = SPARQLWrapper("https://query.wikidata.org/sparql")

query = """
    #Les dix êtres humains les plus lourds
    #defaultView:BubbleChart
    #TEMPLATE={ "template": "The top 10 heaviest ?type ", "variables": { "?type": { "query": "SELECT DISTINCT ?id WHERE { ?i wdt:P2067 ?v. ?i wdt:P31 ?id}" } } }
    SELECT ?item ?itemLabel ?mass
    WHERE {
    {
    SELECT ?item ?mass WHERE {
      ?item wdt:P31 wd:Q5;
            p:P2067/psn:P2067/wikibase:quantityAmount ?mass.
    }
    ORDER BY DESC(?mass)
    LIMIT 10
    }
    SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en" }
    }
    """

sparql.setQuery(query)

sparql.setReturnFormat(JSON)
results = sparql.query().convert()

for result in results["results"]["bindings"]:
    print(result)