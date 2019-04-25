#!/usr/bin/python3
from requests import get
import json


def get_qnumber(wikiarticle):
    resp = get('https://www.wikidata.org/w/api.php', {
        'action': 'wbsearchentities',
        'language': 'en',
        'type': 'item',
        'search': wikiarticle,
        'format': 'json'

    }).json()

    return resp


answer = get_qnumber(wikiarticle="New York")
for page in answer['search']:
    print(page['id'] + " : " + page['description'])
