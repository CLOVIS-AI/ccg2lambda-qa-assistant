from SPARQLWrapper import SPARQLWrapper, JSON

# url where the query has to be sent through the wrapper
sparql = SPARQLWrapper("https://query.wikidata.org/sparql")

query = open("query.sparql", "r")


sparql.setQuery(query.read())

sparql.setReturnFormat(JSON)
results = sparql.query().convert()

for result in results["results"]["bindings"]:
    print(result)