# this package manages the connection with the wiki services.
# It consists in:
#   - Fetching the closest result possible of the user input
#   - Using this result, fetching up to 7 possible wikidata pages
#   - For each page, fetch the most important data: its code, its name, a short description and the page link.
from qalogging import verbose

verbose("Loaded package 'wikidata'")
