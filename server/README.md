# ccg2lambda QA Assistant: Server

This directory stores the code of the server that handles the pipelines.

## Installation & setup

Follow the steps in the main [README](../README.md); they include the procedure to setup this project.

## What does it do?

The goal of this project is to expose a TCP interface from which any client can use the [ccg2lambda](https://github.com/mynlp/ccg2lambda), [depccg](https://github.com/masashi-y/depccg) and [SPARQL](https://en.wikipedia.org/wiki/SPARQL) projects.

The project is split into Python packages:

 - [network](src/network) handles the TCP server. [More information](src/network/README.md)
 - [conversion](src/conversion) handles the conversion from natural language (English) to lambda-expressions; using the following pipeline:
   - Multiple sentences in natural language (English) are annotated and split by [spaCy](https://spacy.io/),
   - The results are converted into CCG trees using [depccg](https://github.com/masashi-y/depccg),
   - The CCG trees are converted into λ-expressions by [ccg2lambda](https://github.com/mynlp/ccg2lambda),
   - The λ-expressions are converted into Abstract Syntax Trees by [ccg2lambda](https://github.com/mynlp/ccg2lambda),
   - The ASTs are parsed into Python objects by [NLTK](https://www.nltk.org/).
   - This pipeline is coded in [converter.py](src/conversion/converter.py); all the steps are private functions, and the function `convert(List[str])->List[Expression]` exposes the pipeline as a unit.
 - [nltk2qo](src/nltk2qo) handles the next step of the conversion: it parses the resulting `Expressions` (the output from the [conversion](src/conversion) package) into `Sentence` objects, which are simplified versions that are more convenient to use when it comes to SPARQL.
   - The `Expression` objects are recursively-parsed by [the nltk_to_query_objects function](src/nltk2qo/converter.py).
   - To see the structure of the generated Sentences, just call that method with any list of `Expression` from the [conversion](src/conversion) package; it will print the structure of the generated objects in an easy to read way.
 - [sparql](src/sparql) Contains SPARQL wrapper and query builder (subpackage [queryBuilder](src/sparql/queryBuilder)):
   - The wrapper is a simple tool that sends a query to a determined endpoint. We use [Wikidata](https://www.wikidata.org/wiki/Wikidata:Main_Page) as our endpoint. For more information, please see on the `Wikidata` section below.
   - The query builder converts the resulting `Expressions` of the package nltk2go into SPARQL queries to be sent to the Wikidata structure in order to retrieve its results.
 - [wikidata](src/wikidata) is a simple package that fetches from the Wiki group unique identifiers used by Wikidata. For more information, please see the `Wikidata` section below.


## Wikidata knowledge & its uses in our project

This project uses the [Wikidata](https://www.wikidata.org/wiki/Wikidata:Main_Page) services to obtain the desired results of our SPARQL queries.
Using such endpoint however requires some knowledge about its way of functionning.

 - As Wikidata uses SPARQL, it has its own tutorial about its use of triples that you can find [here](https://en.wikibooks.org/wiki/SPARQL/Triples).
 - It uses a unique set of `Q-codes` to describe Wikidata items and `P-codes` to describe Wikidata properties. [Find more about Wikidata Identifiers here](https://www.wikidata.org/wiki/Wikidata:Identifiers).
 - Wikidata uses its own [datamodel](https://en.wikibooks.org/wiki/SPARQL/WIKIDATA_Qualifiers,_References_and_Ranks) that has to be known in order to query its elements.
 - Wikidata offers a [Wikidata Query Service](https://query.wikidata.org/) that allows its users to try SPARQL queries on the Wikidata service.
 
Although this lists the most basic data about Wikidata, please note that some information may be missing.

## Use the Command Line Interface (CLI)

A simple CLI is available, written in the files [server.py](src/server.py) and [client.py](src/client.py). It is important to call them from the right directory; for this reason we have added a Make task for both of them, in the project's Makefile.

First, you will need to run the server in a terminal:

        make server

This will setup the project and start the server.

Then, open a new terminal (without killing the server) and run:

        make client

This will start the client. You can now use the `?` (`help`) command to display the list of options.

To close the server, you can press `CTRL+C`: it will detect it and close cleanly.
