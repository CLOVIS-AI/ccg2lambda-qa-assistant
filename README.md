# ccg2lambda QA Assistant

## Introduction

The goal of this project is to setup a pipeline to unify the ccg2lambda project in a single application.

Especially, this project will make it possible to use a single UI to ask a question, and get an answer back.

Here is a simplified version of the pipeline:

 1. The user writes a sentence in the UI (this project)
 1. The sentence is translated into CCG (by C&C or depccg)
 1. The result is translated into a logical formula (by ccg2lambda)
 1. The formula is parsed into Python objects (by nltk)
 1. The formula is translated into a SPARQL query (this project)
 1. The query is executed, the results are parsed back to text (this project)
 1. The result is displayed to the user in the UI (this project)

## How to use

To use the project, first clone it.

Now, run:

`make update`

This should clone the `ccg2lambda` project. To make sure it works well, go into the subdirectory `ccg2lambda` and set it up correctly according to the explaination on the official project's page: https://github.com/mynlp/ccg2lambda

## Packages used by this project

Several packages (in addition of those used by the ccg2lambda project linked before) are used by this application. 

- Wikipedia, the Python library:
           https://pypi.org/project/wikipedia/
- Beautiful Soup, library used for pulling data out from HTML and XML files:
           https://www.crummy.com/software/BeautifulSoup/bs4/doc/
- SPARQLWrapper, Python wrapper around SPARQL (https://en.wikipedia.org/wiki/SPARQL) services:
           https://pypi.org/project/SPARQLWrapper/

