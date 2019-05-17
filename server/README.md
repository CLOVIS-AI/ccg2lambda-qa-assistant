# ccg2lambda QA Assistant: Server

This directory stores the code of the server that handles the pipelines.

## Installation & setup

Follow the steps in the main [README](../README.md); they include the procedure to setup this project.

## What does it do?

The goal of this project is to expose a TCP interface from which any client can use the [ccg2lambda](https://github.com/mynlp/ccg2lambda), [DepCCG](https://github.com/masashi-y/depccg) and SPARQL projects.

The project is split into Python packages:

 - [network](network) handles the TCP server. [More information](network/README.md)
 - [conversion](conversion) handles the conversion from natural language (English) to lambda-expressions; using the following pipeline:
   - Multiple sentences in natural language (English) are annotated and split by [spaCy](https://spacy.io/),
   - The results are converted into CCG trees using [depccg](https://github.com/masashi-y/depccg),
   - The CCG trees are converted into λ-expressions by [ccg2lambda](https://github.com/mynlp/ccg2lambda),
   - The λ-expressions are converted into Abstract Syntax Trees by [ccg2lambda](https://github.com/mynlp/ccg2lambda),
   - The ASTs are parsed into Python objects by [NLTK](https://www.nltk.org/).
   - This pipeline is coded in [converter.py](conversion/converter.py); all the steps are private functions, and the function `convert(List[str])->List[Expression]` exposes the pipeline as a unit.
 - [nltk2qo](nltk2qo) handles the next step of the conversion: it parses the resulting `Expressions` (the output from the [conversion](conversion) package) into `Sentence` objects, which are simplified versions that are more convenient to use when it comes to SPARQL.
   - The `Expression` objects are recursively-parsed by [the nltk_to_query_objects function](nltk2qo/converter.py).
   - To see the structure of the generated Sentences, just call that method with any list of `Expression` from the [conversion](conversion) package; it will print the structure of the generated objects in an easy to read way.
 - [sparql](sparql) [TODO]
 - [wikidata](wikidata) [TODO]
