# this package purpose is to convert natural language into SPARQL requests
#
# In order to run, this package uses the following imports:
#   - ccg2lambda :
#           https://github.com/mynlp/ccg2lambda

#
#   All installation guides are described on their respective link.
#
from pathlib import Path

from depccg.parser import EnglishCCGParser

from conversion.paths import init_paths, MODEL
from qalogging import verbose

init_paths()

depccg_options = dict(
    # A list of binary rules
    # By default: depccg.combinator.en_default_binary_rules
    binary_rules=None,
    # Penalize an application of a unary rule by adding this value (negative log probability)
    unary_penalty=0.1,
    # Prune supertags with low probabilities using this value
    beta=0.00001,
    # Set False if not prune
    use_beta=True,
    # Use category dictionary
    use_category_dict=True,
    # Use seen rules
    use_seen_rules=True,
    # This also used to prune supertags
    pruning_size=50,
    # Nbest outputs
    nbest=1,
    # Limit categories that can appear at the root of a CCG tree
    # By default: S[dcl], S[wq], S[q], S[qem], NP.
    possible_root_cats=None,
    # Give up parsing long sentences
    max_length=250,
    # Give up parsing if it runs too many steps
    max_steps=100000,
    # You can specify a GPU
    gpu=-1
)

depccg_model = Path(MODEL)

depccg_parser = EnglishCCGParser.from_dir(
    depccg_model,
    load_tagger=True,
    **depccg_options
)

verbose("Loaded package 'conversion'")
